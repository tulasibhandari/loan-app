#tools/template_debugger.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import re
from docxtpl import DocxTemplate

from services.prepare_report_contexts import prepare_report_context

def extract_placeholders(template_path):
    """Extract all placeholders from a .docx template"""
    doc = DocxTemplate(template_path)
    return doc.get_undeclared_template_variables()



def  compare_template_with_context(template_path, member_number):
    """Compare template placeholders with actual context keys"""
    print("✅ Starting template comparison...")
    print(f"📄 Template: {template_path}")
    print(f"👤 Member Number: {member_number}")

    placeholders = extract_placeholders(template_path)
    context = prepare_report_context(member_number)
    context_keys = set(context.keys())

    print("🧪 Placeholders found in template:", placeholders)
    print("🧪 Keys in context:", context_keys)

    missing_in_context = placeholders - context_keys
    extra_in_context = context_keys - placeholders

    print("🔍 Placeholders in Template but Missing in Context:")
    for item in sorted(missing_in_context):
        print(f" - {item}")
    
    print("\n✅ Placeholders in Context but not used in Template:")
    for item in sorted(extra_in_context):
        print(f"- {item}")
    
if __name__ == "__main__":
        if len(sys.argv) != 3:
            print("Usage: python tools/template_debugger.py <template_path> <member_number>")
        else:
            template_path = sys.argv[1]
            member_number = sys.argv[2]
            compare_template_with_context(template_path, member_number)   