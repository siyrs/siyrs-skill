#!/usr/bin/env python3
"""Unified deterministic helper CLI for siyrs-skill."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from collect_git_changes import collect
from command_registry import registry_document
from detect_project import detect
from fingerprint import fingerprint
from route_command import route
from scan_secrets import scan
from validate_bundle import validate

def main()->int:
    p=argparse.ArgumentParser(prog='siyk'); sub=p.add_subparsers(dest='command',required=True)
    r=sub.add_parser('route'); r.add_argument('text'); r.add_argument('--root',default=str(Path(__file__).resolve().parents[1]))
    reg=sub.add_parser('registry'); reg.add_argument('--root',default=str(Path(__file__).resolve().parents[1]))
    d=sub.add_parser('detect'); d.add_argument('--root',default='.')
    c=sub.add_parser('changes'); c.add_argument('--root',default='.'); c.add_argument('--base'); c.add_argument('--purpose',choices=['t1','add','generic'],default='t1')
    f=sub.add_parser('fingerprint'); f.add_argument('--root',default='.')
    s=sub.add_parser('scan'); s.add_argument('--root',default='.'); s.add_argument('--all',action='store_true')
    v=sub.add_parser('validate'); v.add_argument('--root',default='.')
    a=p.parse_args()
    try:
        if a.command=='route': result=route(a.text,Path(a.root)); code=0 if result['matched'] and result['valid'] else (2 if result['matched'] else 1)
        elif a.command=='registry': result=registry_document(Path(a.root)); code=0
        elif a.command=='detect': result=detect(Path(a.root)); code=0
        elif a.command=='changes': result=collect(Path(a.root),a.base,a.purpose); code=0 if result.get('is_git_repository') else 1
        elif a.command=='fingerprint': result=fingerprint(Path(a.root)); code=0
        elif a.command=='scan': result=scan(Path(a.root),not a.all); code=2 if result['high_confidence_block'] else 0
        else: result=validate(Path(a.root)); code=0 if result['valid'] else 1
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        result={'error':str(exc)}; code=1
    print(json.dumps(result,ensure_ascii=False,indent=2)); return code
if __name__=='__main__': raise SystemExit(main())
