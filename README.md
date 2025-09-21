# Replace strings
Replace all from:
invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->getDataDir()Ljava/io/File;
invoke-virtual {p0, v0}, Lcom/mojang/minecraftpe/MainActivity;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;

To:
invoke-static {}, Landroid/os/Environment;->getExternalStorageDirectory()Ljava/io/File;

# Add permission request:
Paste this method in MainActivity:
.method public checkFirstRunAndRequestPermission()V
    .locals 8
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "NewApi"
        }
    .end annotation

  .prologue
  const/4 v7, 0x0
  const/4 v6, 0x1
  const/4 v5, 0x0
  const-string v3, "app_prefs"
  const-string v4, "is_first_run"
  invoke-virtual {p0, v3, v5}, Landroid/app/Activity;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
  move-result-object v0
  .local v0, "prefs":Landroid/content/SharedPreferences;
  invoke-interface {v0, v4, v6}, Landroid/content/SharedPreferences;->getBoolean(Ljava/lang/String;Z)Z
  move-result v1
  .local v1, "isFirstRun":Z
  if-nez v1, :cond_0
  return-void
  :cond_0
  invoke-interface {v0}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
  move-result-object v2
  .local v2, "editor":Landroid/content/SharedPreferences$Editor;
  invoke-interface {v2, v4, v5}, Landroid/content/SharedPreferences$Editor;->putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;
  invoke-interface {v2}, Landroid/content/SharedPreferences$Editor;->apply()V
  sget v3, Landroid/os/Build$VERSION;->SDK_INT:I
  const/16 v4, 0x1e
  if-lt v3, v4, :cond_1
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
  :cond_1
  return-void
.end method

# After adding checkFirstRunAndRequestPermission()V, add this string to the start of OnCreate:
invoke-virtual {p0}, Lcom/mojang/minecraftpe/MainActivity;->checkFirstRunAndRequestPermission()V

# Add permissions in AndroidManifest.xml
Paste anywhere <uses-permission  android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
