# build_setup.py - Fixed PyQt5 App Bundling Configuration
import sys
import os
import shutil
from pathlib import Path
import sqlite3
import zipfile

# PyInstaller configuration
PYINSTALLER_CONFIG = {
    'app_name': 'LoanDesktopApp',
    'main_script': 'main.py',  # Changed to use main.py directly
    'icon_file': 'assets/icons/app_icon.ico',
    'version_file': 'version_info.txt',
    'company_name': 'Manakamana Saving & Credit Cooperative Society Pvt. Ltd',
    'app_version': '1.0.0',
    'description': 'Loan Management Desktop Application'
}

class AppBundler:
    """Complete PyQt5 Application Bundler"""
    def __init__(self):
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / 'build'
        self.dist_dir = self.project_root / 'dist'
        self.assets_dir = self.project_root / 'assets'
        self.data_dir = self.project_root / 'data'
    
    def setup_directory_structure(self):
        """Create proper directory structure for bundling"""
        directories = [
            'assets/icons',
            'assets/images',
            'data',
            'build',
            'dist',
            'temp'
        ]

        for directory in directories:
            (self.project_root / directory).mkdir(parents=True, exist_ok=True)
        print("✅ Directory structure created!")
    
    def verify_main_script(self):
        """Verify main script exists"""
        main_script = self.project_root / PYINSTALLER_CONFIG['main_script']
        if not main_script.exists():
            print(f"❌ Main script not found: {main_script}")
            return False
        print("✅ Main script verified")
        return True
    
    def prepare_database(self):
        """Prepare database for bundling"""
        source_db = self.data_dir / 'loan_app.db'
        bundle_db = self.data_dir / 'loan_app_bundle.db'

        if source_db.exists():
            try:
                shutil.copy2(source_db, bundle_db)
                print(f"✅ Database prepared: {bundle_db}")
            except Exception as e:
                print(f"❌ Error copying database: {e}")
                self.create_empty_database(bundle_db)
        else:
            print("⚠️ Source database not found, creating empty one")
            self.create_empty_database(bundle_db)
    
    def create_empty_database(self, db_path):
        """Create empty database with proper schema"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                member_number TEXT UNIQUE,
                member_name TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            conn.commit()
            conn.close()
            print(f"✅ Empty database created: {db_path}")
        except Exception as e:
            print(f"❌ Error creating database: {e}")

    def create_spec_file(self):
        """Create PyInstaller spec file"""
        spec_content = f'''# {PYINSTALLER_CONFIG["app_name"]}.spec
# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['{PYINSTALLER_CONFIG["main_script"]}'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('assets', 'assets'),
        ('ui', 'ui'),
        ('services', 'services'),
        ('fonts', 'fonts'),
        ('templates', 'templates'),
        ('icons', 'icons'),
        ('F:/Tuski/extras/pycodes/loan_app/venv/Lib/site-packages/nepali_datetime/data/calendar_bs.csv','nepali_datetime/data')
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'sqlite3'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{PYINSTALLER_CONFIG["app_name"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{PYINSTALLER_CONFIG["icon_file"]}',
)
'''
        spec_file = self.project_root / f"{PYINSTALLER_CONFIG['app_name']}.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print(f"✅ Spec file created: {spec_file}")

    def run_full_bundle_process(self):
        """Run the complete bundling process"""
        print("🚀 Starting PyQt5 App Bundling Process...")
        
        try:
            self.setup_directory_structure()
            if not self.verify_main_script():
                return False
            self.prepare_database()
            self.create_spec_file()
            
            print("\n✅ Bundling preparation complete!")
            print("\n⚡ Run the following command to build:")
            print("pyinstaller {}.spec".format(PYINSTALLER_CONFIG['app_name']))
            return True
            
        except Exception as e:
            print(f"❌ Error during bundling: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    bundler = AppBundler()
    success = bundler.run_full_bundle_process()
    
    if success:
        print("\n🎉 Ready to bundle!")
    else:
        print("\n❌ Bundling preparation failed")