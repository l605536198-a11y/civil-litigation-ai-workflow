#!/usr/bin/env python3
import argparse, json, shutil
from datetime import datetime
from pathlib import Path

FOLDERS=["①当事人提供材料","②诉讼文件","③立案文件","④流程性文件","⑤归档文件"]

def classify(p:Path):
    n=p.name
    court=["传票","保全裁定","保全回执","受理通知","举证通知","缴费通知","送达回证","开庭通知","法院通知"]
    if any(x in n for x in court): return FOLDERS[3]
    if p.suffix.lower()==".pdf" and any(x in n for x in ["签字版","签章版","盖章版","提交版","法院收件"]): return FOLDERS[2]
    if any(x in n for x in ["归档PDF合集","卷宗目录","结案小结","归档结案"]): return FOLDERS[4]
    if p.suffix.lower()==".pdf": return FOLDERS[1]
    if p.suffix.lower() in {".docx",".xlsx",".pptx",".md",".html",".json"}: return FOLDERS[1]
    return FOLDERS[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("workspace_root"); ap.add_argument("case_name")
    ap.add_argument("--source"); ap.add_argument("--copy",action="store_true")
    args=ap.parse_args()
    root=Path(args.workspace_root)/args.case_name; root.mkdir(parents=True,exist_ok=True)
    for f in FOLDERS:(root/f).mkdir(exist_ok=True)
    registry={"case_name":args.case_name,"created_at":datetime.now().astimezone().isoformat(timespec="seconds"),"folders":FOLDERS,"files":[],"rules":{"party_material":"preserve_original","filing_pdf":"signed_or_stamped_only","deadline_reminder":"deadline_minus_1_day_09:00","archive":"cover_catalogue_pdf_bundle"}}
    if args.source:
        src=Path(args.source)
        for p in sorted(src.rglob("*")):
            if not p.is_file() or root in p.parents or p.name.endswith((".inspect.ndjson",".layout.json")) or any(x in str(p) for x in ["_QA_","PPT预览","PPT美化版预览","QA_render","converted"]): continue
            if "自动归档成果" in str(p) and "归档PDF合集" not in p.name: continue
            dest_dir=root/classify(p); dest=dest_dir/p.name
            if args.copy:
                if dest.exists(): dest=dest.with_name(f"{dest.stem}_{p.parent.name}{dest.suffix}")
                shutil.copy2(p,dest)
            registry["files"].append({"source":str(p),"target_folder":dest_dir.name,"copied_to":str(dest) if args.copy else None})
    (root/"案件工作区登记.json").write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding="utf-8")
    deadline={"schema_version":"1.0","reminder_rule":"截止日前一日09:00提醒；无实际送达日不计算、不创建提醒","items":[]}
    (root/FOLDERS[3]/"程序文件登记与期限提醒.json").write_text(json.dumps(deadline,ensure_ascii=False,indent=2),encoding="utf-8")
    (root/FOLDERS[0]/"材料接收说明.txt").write_text("本目录仅保存当事人提供的原始材料和初步证据，不覆盖、不改名原件。\n",encoding="utf-8")
    (root/FOLDERS[2]/"立案文件准入说明.txt").write_text("本目录只保存已经当事人签字或律所盖章、可提交法院的PDF版本。\n",encoding="utf-8")
    print(root)

if __name__=="__main__": main()

