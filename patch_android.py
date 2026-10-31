from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
android = root / "android"
if not android.exists():
    raise SystemExit("Android project folder is missing. Run flutter create --platforms=android . first.")

kts = android / "app" / "build.gradle.kts"
groovy = android / "app" / "build.gradle"

if kts.exists():
    source = kts.read_text(encoding="utf-8")
    source = re.sub(r"compileSdk\s*=\s*[^\n]+", "compileSdk = 37", source, count=1)
    source = re.sub(r"minSdk\s*=\s*[^\n]+", "minSdk = 26", source, count=1)
    source = re.sub(r"sourceCompatibility\s*=\s*JavaVersion\.VERSION_\d+", "sourceCompatibility = JavaVersion.VERSION_17", source)
    source = re.sub(r"targetCompatibility\s*=\s*JavaVersion\.VERSION_\d+", "targetCompatibility = JavaVersion.VERSION_17", source)
    source = re.sub(r"jvmTarget\s*=\s*[^\n]+", 'jvmTarget = "17"', source)
    kts.write_text(source, encoding="utf-8")
elif groovy.exists():
    source = groovy.read_text(encoding="utf-8")
    source = re.sub(r"compileSdkVersion\s+[^\n]+", "compileSdkVersion 37", source, count=1)
    source = re.sub(r"compileSdk\s+[^\n]+", "compileSdk 37", source, count=1)
    source = re.sub(r"minSdkVersion\s+[^\n]+", "minSdkVersion 26", source, count=1)
    source = re.sub(r"minSdk\s+[^\n]+", "minSdk 26", source, count=1)
    source = re.sub(r"sourceCompatibility\s+JavaVersion\.VERSION_\d+", "sourceCompatibility JavaVersion.VERSION_17", source)
    source = re.sub(r"targetCompatibility\s+JavaVersion\.VERSION_\d+", "targetCompatibility JavaVersion.VERSION_17", source)
    source = re.sub(r"jvmTarget\s*=\s*['\"]?[^\n'\"]+['\"]?", "jvmTarget = '17'", source)
    groovy.write_text(source, encoding="utf-8")
else:
    raise SystemExit("Could not find android/app/build.gradle(.kts).")

manifest = android / "app" / "src" / "main" / "AndroidManifest.xml"
if manifest.exists():
    source = manifest.read_text(encoding="utf-8")
    source = re.sub(r'android:label="[^"]*"', 'android:label="TUN VPNSOPR"', source, count=1)
    if "android.permission.CAMERA" not in source:
        source = re.sub(
            r"(<manifest\b[^>]*>)",
            r'\1\n    <uses-permission android:name="android.permission.CAMERA" />',
            source,
            count=1,
        )
    manifest.write_text(source, encoding="utf-8")

print("Android settings patched: compileSdk=37, minSdk=26, Java 17, camera permission, app label=TUN VPNSOPR")
