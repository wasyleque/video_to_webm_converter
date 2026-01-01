import os
import subprocess
import argparse
import sys

# Lista rozszerzeń plików wideo do konwersji (małymi literami)
VIDEO_EXTENSIONS = (
    '.avi', '.vid', '.mov', '.mp4', '.mp5', '.mpeg', '.ts', '.mkv', '.wmv', '.flv', '.m4v'
)

def format_size(size_bytes):
    """Konwertuje rozmiar w bajtach na czytelny format (KB, MB, GB)."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

def check_ffmpeg():
    """Sprawdza, czy polecenie ffmpeg jest dostępne w systemie."""
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("BŁĄD: Narzędzie 'ffmpeg' nie jest zainstalowane lub nie ma go w ścieżce systemowej (PATH).")
        print("Proszę zainstalować ffmpeg, aby kontynuować.")
        print("Na systemach Debian/Ubuntu: sudo apt update && sudo apt install ffmpeg")
        return False

def convert_videos(root_dir, autoremove, recursive):
    """Główna funkcja do wyszukiwania i konwertowania plików wideo."""
    total_original_size = 0
    total_converted_size = 0
    converted_files_count = 0
    failed_files = []
    files_to_process = []

    if recursive:
        print(f"Rozpoczynam REKURSYWNE przeszukiwanie folderu '{root_dir}'...")
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(VIDEO_EXTENSIONS):
                    files_to_process.append(os.path.join(subdir, file))
    else:
        print(f"Rozpoczynam przeszukiwanie folderu '{root_dir}' (bez podfolderów)...")
        for file in os.listdir(root_dir):
            path = os.path.join(root_dir, file)
            if os.path.isfile(path) and file.lower().endswith(VIDEO_EXTENSIONS):
                files_to_process.append(path)

    if not files_to_process:
        print("Nie znaleziono pasujących plików wideo do konwersji.")
    else:
        print(f"Znaleziono {len(files_to_process)} plików do przetworzenia.")


    for source_path in files_to_process:
        target_path = os.path.splitext(source_path)[0] + '.webm'

        # Pomiń, jeśli plik .webm już istnieje
        if os.path.exists(target_path):
            print(f"Pominięto: Plik docelowy '{target_path}' już istnieje.")
            continue

        try:
            original_size = os.path.getsize(source_path)
            print(f"\n--- Konwertowanie: {source_path} ({format_size(original_size)}) ---")

            # Polecenie ffmpeg:
            # -i: plik wejściowy
            # -c:v libvpx-vp9: kodek wideo VP9 (standard dla WebM)
            # -crf 30: stały współczynnik jakości (0-63, im wyższy, tym niższa jakość i mniejszy plik)
            # -b:v 0: zmienny bitrate
            # -c:a libopus: kodek audio Opus (standard dla WebM)
            # -n: nie nadpisuj pliku wyjściowego, jeśli istnieje
            ffmpeg_command = [
                'ffmpeg', '-i', source_path,
                '-c:v', 'libvpx-vp9', '-crf', '30', '-b:v', '0',
                '-c:a', 'libopus',
                '-n', target_path
            ]

            # Uruchomienie konwersji, ukrywając logi ffmpeg dla czystszego wyjścia
            process = subprocess.run(
                ffmpeg_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            converted_size = os.path.getsize(target_path)
            saved_space = original_size - converted_size
            print(f"Sukces! Nowy plik: {target_path} ({format_size(converted_size)})")
            print(f"Zaoszczędzono: {format_size(saved_space)}")

            total_original_size += original_size
            total_converted_size += converted_size
            converted_files_count += 1

            if autoremove:
                print(f"Usuwanie oryginalnego pliku: {source_path}")
                os.remove(source_path)

        except subprocess.CalledProcessError as e:
            print(f"BŁĄD podczas konwersji pliku {source_path}.")
            print(f"Stderr: {e.stderr}")
            failed_files.append(source_path)
            # Usuń częściowo utworzony plik .webm w razie błędu
            if os.path.exists(target_path):
                os.remove(target_path)
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd przy pliku {source_path}: {e}")
            failed_files.append(source_path)

    # --- Podsumowanie ---
    print("\n================== PODSUMOWANIE ==================")
    if converted_files_count > 0:
        total_saved = total_original_size - total_converted_size
        print(f"Pomyślnie przekonwertowano: {converted_files_count} plików.")
        print(f"Łączny rozmiar oryginalny: {format_size(total_original_size)}")
        print(f"Łączny rozmiar po konwersji: {format_size(total_converted_size)}")
        print(f"Całkowita oszczędność miejsca: {format_size(total_saved)}")
    else:
        print("Nie zakończono pomyślnie żadnej nowej konwersji.")

    if failed_files:
        print("\nNie udało się przekonwertować następujących plików:")
        for f in failed_files:
            print(f"- {f}")
    print("==================================================")


def main():
    """Główna funkcja programu."""
    if not check_ffmpeg():
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Konwertuje pliki wideo do formatu .webm. Domyślnie działa tylko w bieżącym folderze.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--autoremove',
        action='store_true',
        help='Usuwa oryginalny plik wideo po pomyślnej konwersji.'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Przeszukuje foldery rekursywnie (w głąb).'
    )
    args = parser.parse_args()

    current_directory = '.'
    convert_videos(current_directory, args.autoremove, args.recursive)

if __name__ == '__main__':
    main()
