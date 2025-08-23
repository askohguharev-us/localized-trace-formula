import argparse, os, re, pathlib, sys

BEGIN = re.compile(r'^\s*%%%BEGIN_PRIVATE')
END   = re.compile(r'^\s*%%%END_PRIVATE')

def process_file(src_path, dst_path):
    keep = True
    out = []
    for line in open(src_path, 'r', encoding='utf-8', errors='ignore'):
        if BEGIN.search(line): 
            keep = False
            continue
        if END.search(line): 
            keep = True
            continue
        if keep: out.append(line)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.writelines(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', default='PUBLIC')
    ap.add_argument('--in', dest='inp', required=True)
    ap.add_argument('--out', dest='out', required=True)
    args = ap.parse_args()
    for root, _, files in os.walk(args.inp):
        for fn in files:
            if not fn.endswith('.tex'): 
                continue
            src = os.path.join(root, fn)
            rel = os.path.relpath(src, args.inp)
            dst = os.path.join(args.out, rel)
            process_file(src, dst)

if __name__ == '__main__':
    main()
