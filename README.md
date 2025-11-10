# Replace strings
Replace all strings from:
```
invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->getDataDir()Ljava/io/File;
```
```
invoke-virtual {p0, v0}, Lcom/mojang/minecraftpe/MainActivity;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;
```

To:
```
invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;
```

# Add permission request:
Paste this method in MainActivity:
```
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
```
# After adding checkFirstRunAndRequestPermission()V, add this string to the start of OnCreate:
```
invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->checkFirstRunAndRequestPermission()V
```
It should look like this:
<img width="1013" height="242" alt="Screenshot_20251110_214449_MT Manager" src="https://github.com/user-attachments/assets/3cfde89f-5928-41f4-bf5c-bf1610f4033a" />

# Add permissions in AndroidManifest.xml
Paste this anywhere:
```
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
```
