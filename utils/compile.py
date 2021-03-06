import shutil
import sys
from pathlib import Path

import mpy_cross

# mpy_cross.run('--help')


def compile(src_path, dst_path, skip_files):
    cwd = Path().cwd()

    print('Compile files from:', src_path)
    for file_path in sorted(src_path.glob('*.py')):
        file_path = file_path.relative_to(cwd)

        if file_path.name in skip_files:
            continue

        output_path = Path(dst_path, file_path.name).with_suffix('.mpy')
        output_path = output_path.relative_to(cwd)

        print(f' + {file_path} -> {output_path}')

        # http://docs.micropython.org/en/latest/library/micropython.html#micropython.opt_level
        # Currently the highest optimize level is 3, see:
        # https://github.com/micropython/micropython/issues/5392#issuecomment-562847197
        mpy_cross.run(
            # '-O2',  # exceptions can report the line number they occurred at
            '-O3',  # highest optimize level: code line in tracebacks are always 1
            '-v',
            '-v',
            '-v',
            str(file_path),
            '-o', str(output_path)
        )


def create_bdist(src_path, dst_path, ignore_files, copy_files, copy_file_pattern):
    src_path = src_path.resolve()
    dst_path = dst_path.resolve()
    dst_path.mkdir(exist_ok=True)
    compile(
        src_path=src_path,
        dst_path=dst_path,
        skip_files=list(copy_files) + list(ignore_files),
    )
    print(' -' * 50)
    print('Copy files...')
    cwd = Path().cwd()
    files2copy = set([Path(src_path, n) for n in copy_files])
    for pattern in copy_file_pattern:
        files2copy.update(set(src_path.glob(pattern)))

    for file_path in files2copy:
        if file_path.name in ignore_files:
            continue

        file_path = file_path.resolve().relative_to(cwd)
        output_path = Path(dst_path, file_path.name).relative_to(cwd)
        print(f' + {file_path} -> {output_path}')
        try:
            shutil.copyfile(file_path, output_path)
        except FileNotFoundError as e:
            print(f'ERROR: {e}', file=sys.stderr)
