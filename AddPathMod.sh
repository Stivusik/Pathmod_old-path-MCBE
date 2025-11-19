if [ -n "$1" ] && [ -d "$1" ]; then
  cd "$1" || exit 1
fi

TARGET="invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->getDataDir()Ljava/io/File;"
REPLACE="invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;"
for DIR in smali smali_classes2; do
  if [ ! -d "$DIR" ]; then
    continue
  fi
  for FILE in MainActivity.smali; do
    PATH_TO_FILE="${DIR}/com/mojang/minecraftpe/${FILE}"
    if [ -f "$PATH_TO_FILE" ]; then
      TMP="${PATH_TO_FILE}.tmp"
      sed "s|$TARGET|$REPLACE|g" "$PATH_TO_FILE" > "$TMP" &&
      mv "$TMP" "$PATH_TO_FILE"
    fi
  done
done

if [ -n "$1" ] && [ -d "$1" ]; then
  cd "$1" || exit 1
fi
TARGET="invoke-virtual {p0, v0}, Lcom/mojang/minecraftpe/MainActivity;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;"
REPLACE="invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;"
for DIR in smali smali_classes2; do
  if [ ! -d "$DIR" ]; then
    continue
  fi
  for FILE in MainActivity.smali; do
    PATH_TO_FILE="${DIR}/com/mojang/minecraftpe/${FILE}"
    if [ -f "$PATH_TO_FILE" ]; then
      TMP="${PATH_TO_FILE}.tmp"
      sed "s|$TARGET|$REPLACE|g" "$PATH_TO_FILE" > "$TMP" &&
      mv "$TMP" "$PATH_TO_FILE"
    fi
  done
done

read -r -d '' NEW_METHOD <<'EOF'
.method public checkFirstRunAndRequestPermission()V
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
EOF

for DIR in smali smali_classes2; do
  if [ ! -d "$DIR" ]; then
    continue
  fi
  
  PATH_TO_FILE="${DIR}/com/mojang/minecraftpe/MainActivity.smali"
  
  if [ -f "$PATH_TO_FILE" ]; then
    if ! grep -q "checkFirstRunAndRequestPermission" "$PATH_TO_FILE"; then
      printf "\n%s\n" "${NEW_METHOD}" >> "$PATH_TO_FILE"
    fi
    
    INVOKE_LINE='invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->checkFirstRunAndRequestPermission()V'
    if ! grep -Fq "$INVOKE_LINE" "$PATH_TO_FILE"; then
        TARGET_ANCHOR='const-string v0, "MinecraftPlatform"'
        LINE_TO_INSERT="    ${INVOKE_LINE}"
        ESCAPED_INSERT=$(printf '%s\n' "$LINE_TO_INSERT" | sed 's:[&/\]:\\&:g')
        sed -i "/${TARGET_ANCHOR}/i ${ESCAPED_INSERT}" "$PATH_TO_FILE"
    fi
  fi
done

MANIFEST="AndroidManifest.xml"

if [ -f "$MANIFEST" ]; then
  sed -i 's|</manifest>|    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />\n</manifest>|' "$MANIFEST"
  sed -i 's|</manifest>|    <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />\n</manifest>|' "$MANIFEST"
fi
exit 0
