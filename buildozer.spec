[app]

# (str) Title of your application
title = My Application

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,requests

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) Android AAR archives to add (currently works only with sdl2 bootstraps)
#android.add_aars =

# (list) Gradle dependencies to add (currently works only with sdl2 bootstraps)
#android.gradle_dependencies =

# (list) add java compile options
#android.add_compile_options =

# (list) Java classes to add as activities to the manifest.
#android.add_activities =

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
#android.sdk = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android package name
#android.package = org.test.myapp

# (int) Android version code
#android.version_code = 1

# (list) Android permissions to add
#android.permissions = INTERNET

# (str) Android API to use
#android.api = 27

# (str) Android minimum API to use
#android.minapi = 21

# (str) Android NDK API to use (optional)
#android.ndk_api = 21

# (str) Android build tools version
android.build_tools_version = 34.0.0

# (bool) Accept SDK licenses automatically
android.accept_sdk_license = True
