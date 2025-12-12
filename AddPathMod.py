#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile

def replace_in_file_literal(path, old, new):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    if old not in data:
        return False
    newdata = data.replace(old, new)
    fd, tmpname = tempfile.mkstemp(dir=os.path.dirname(path))
    os.close(fd)
    with open(tmpname, "w", encoding="utf-8") as f:
        f.write(newdata)
    shutil.move(tmpname, path)
    return True

def file_contains_literal(path, literal):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return literal in f.read()
    except FileNotFoundError:
        return False

def insert_line_before_anchor(path, anchor, line_to_insert):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return False

    for i, ln in enumerate(lines):
        if anchor in ln:
            if not line_to_insert.endswith("\n"):
                line_to_insert += "\n"
            line_to_insert += "\n"
            lines.insert(i, line_to_insert)

            with open(path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True

    return False


def main():
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        try:
            os.chdir(sys.argv[1])
        except Exception:
            sys.exit(1)

    TARGET = "invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->getDataDir()Ljava/io/File;"
    REPLACE = "invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;"
    for DIR in ("smali", "smali_classes2", "smali_classes4"):
        if not os.path.isdir(DIR):
            continue
        PATH = os.path.join(DIR, "com", "mojang", "minecraftpe", "MainActivity.smali")
        if os.path.isfile(PATH):
            replace_in_file_literal(PATH, TARGET, REPLACE)

    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        try:
            os.chdir(sys.argv[1])
        except Exception:
            sys.exit(1)

    TARGET = "invoke-virtual {p0, v0}, Lcom/mojang/minecraftpe/MainActivity;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;"
    REPLACE = "invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;"
    for DIR in ("smali", "smali_classes2", "smali_classes4"):
        if not os.path.isdir(DIR):
            continue
        PATH = os.path.join(DIR, "com", "mojang", "minecraftpe", "MainActivity.smali")
        if os.path.isfile(PATH):
            replace_in_file_literal(PATH, TARGET, REPLACE)

    NEW_METHOD = r'''.method public RequestPermission()V
    .registers 9
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "NewApi"
        }
    .end annotation

    .prologue
    const/4 v7, 0x0
    const/4 v6, 0x1
    const/4 v5, 0x0

    sget v3, Landroid/os/Build$VERSION;->SDK_INT:I

    const/16 v4, 0x1e

    if-lt v3, v4, :cond_39

    invoke-static {}, Landroid/os/Environment;->isExternalStorageManager()Z

    move-result v3

    if-nez v3, :cond_39

    new-instance v3, Landroid/content/Intent;

    sget-object v4, Landroid/provider/Settings;->ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION:Ljava/lang/String;

    invoke-direct {v3, v4}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V

    const-string v4, "package"

    invoke-virtual {p0}, Landroid/app/Activity;->getPackageName()Ljava/lang/String;
    move-result-object v5

    invoke-static {v4, v5, v7}, Landroid/net/Uri;->fromParts(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Landroid/net/Uri;
    move-result-object v4

    invoke-virtual {v3, v4}, Landroid/content/Intent;->setData(Landroid/net/Uri;)Landroid/content/Intent;

    invoke-virtual {p0, v3}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V

    :cond_39
    return-void
.end method
'''

    for DIR in ("smali", "smali_classes2", "smali_classes4"):
        if not os.path.isdir(DIR):
            continue

        PATH = os.path.join(DIR, "com", "mojang", "minecraftpe", "MainActivity.smali")
        if not os.path.isfile(PATH):
            continue

        if not file_contains_literal(PATH, ".method public RequestPermission()V"):
            with open(PATH, "a", encoding="utf-8") as f:
                f.write("\n\n" + NEW_METHOD + "\n")

        INVOKE_LINE = '    invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->RequestPermission()V'
        if not file_contains_literal(PATH, INVOKE_LINE.strip()):
            TARGET_ANCHOR = 'const-string v0, "MinecraftPlatform"'
            insert_line_before_anchor(PATH, TARGET_ANCHOR, INVOKE_LINE)

    MANIFEST = "AndroidManifest.xml"
    if os.path.isfile(MANIFEST):

        with open(MANIFEST, "r", encoding="utf-8") as f:
            data = f.read()
        if "</manifest>" in data:
            data = data.replace(
                "</manifest>",
                '    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />\n</manifest>',
                1
            )
            with open(MANIFEST, "w", encoding="utf-8") as f:
                f.write(data)

        with open(MANIFEST, "r", encoding="utf-8") as f:
            data = f.read()
        if "</manifest>" in data:
            data = data.replace(
                "</manifest>",
                '    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />\n</manifest>',
                1
            )
            with open(MANIFEST, "w", encoding="utf-8") as f:
                f.write(data)

    print("Added.")
    sys.exit(0)


if __name__ == "__main__":
    main()
