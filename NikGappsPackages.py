from Config import TARGET_ANDROID_VERSION
from Config import ADB_ROOT_ENABLED
from NikGapps.Helper import Constants
from NikGapps.Helper.AddonSet import AddonSet
from NikGapps.Helper.Package import Package
from NikGapps.Helper.AppSet import AppSet


class NikGappsPackages:
    all_packages = "full"

    @staticmethod
    def get_packages(package_type):
        if str(package_type).lower() == "go":
            return NikGappsPackages.get_go_package()
        if str(package_type).lower() == "core":
            return NikGappsPackages.get_core_package()
        if str(package_type).lower() == "basic":
            return NikGappsPackages.get_basic_package()
        if str(package_type).lower() == "omni":
            return NikGappsPackages.get_omni_package()
        if str(package_type).lower() == "stock":
            return NikGappsPackages.get_stock_package()
        if str(package_type).lower() == "full":
            return NikGappsPackages.get_full_package()
        if str(package_type).lower() == "addons":
            addon_set_list = AddonSet.get_addon_packages()
            return addon_set_list
        if str(package_type).lower() == "addonsets":
            addon_set_list = []
            for app_set in NikGappsPackages.get_full_package():
                if app_set in ['Core', 'CoreGo']:
                    continue
                addon_set_list.append(app_set)
            return addon_set_list
        else:
            addon_set_list = AddonSet.get_addon_packages(package_type)
            if addon_set_list is None:
                for app_set in NikGappsPackages.get_full_package():
                    if str(app_set.title).lower() == str(package_type).lower():
                        return [app_set]
                return [None]
            else:
                return addon_set_list

    @staticmethod
    def get_app_set(pkg: Package, title=None):
        if title is None:
            name = pkg.package_title
        else:
            name = title
        return AppSet(name, [pkg])

    @staticmethod
    def get_go_package():
        extra_files_go = Package("ExtraFilesGo", None, None)
        extra_files_go.predefined_file_list.append("etc/default-permissions/default-permissions.xml")
        extra_files_go.predefined_file_list.append("etc/default-permissions/opengapps-permissions.xml")
        extra_files_go.predefined_file_list.append("etc/permissions/privapp-permissions-google.xml")
        extra_files_go.predefined_file_list.append("etc/permissions/privapp-permissions-hotword.xml")
        if TARGET_ANDROID_VERSION == 9:
            extra_files_go.predefined_file_list.append("etc/permissions/privapp-permissions-google-product.xml")
            extra_files_go.predefined_file_list.append("etc/permissions/privapp-permissions-elgoog.xml")
        if TARGET_ANDROID_VERSION == 10:
            extra_files_go.predefined_file_list.append("etc/permissions/privapp-permissions-google-p.xml")
            extra_files_go.predefined_file_list.append("etc/permissions/privapp-permissions-google-ps.xml")
            extra_files_go.predefined_file_list.append("etc/permissions/split-permissions-google.xml")
        extra_files_go.additional_installer_script = """script_text="<permissions>
                            <!-- Shared library required on the device to get Google Dialer updates from
                                 Play Store. This will be deprecated once Google Dialer play store
                                 updates stop supporting pre-O devices. -->
                            <library name=\\"com.google.android.dialer.support\\"
                              file=\\"$install_partition/framework/com.google.android.dialer.support.jar\\" />

                            <!-- Starting from Android O and above, this system feature is required for
                                 getting Google Dialer play store updates. -->
                            <feature name=\\"com.google.android.apps.dialer.SUPPORTED\\" />
                        </permissions>"
                        echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.dialer.support.xml
                        set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.dialer.support.xml"
                        installPath=$product_prefix"etc/permissions/com.google.android.dialer.support.xml"
                        echo "install=$installPath" >> /tmp/addon/$packagePath
                        if [ -f "$install_partition/etc/permissions/com.google.android.dialer.support.xml" ]; then
                          addToLog "- $install_partition/etc/permissions/com.google.android.dialer.support.xml Successfully Written!"
                        fi"""
        extra_files_go.additional_installer_script += """
                        script_text="<permissions>
                            <library name=\\"com.google.android.maps\\"
                                    file=\\"$install_partition/framework/com.google.android.maps.jar\\" />
                        </permissions>"
                        echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.maps.xml
                        set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.maps.xml"
                        installPath=$product_prefix"etc/permissions/com.google.android.maps.xml"
                        echo "install=$installPath" >> /tmp/addon/$packagePath
                        if [ -f "$install_partition/etc/permissions/com.google.android.maps.xml" ]; then
                          addToLog "- $install_partition/etc/permissions/com.google.android.maps.xml Successfully Written!"
                        fi"""
        extra_files_go.additional_installer_script += """
                                script_text="<permissions>
                    <library name=\\"com.google.widevine.software.drm\\"
                        file=\\"/system/product/framework/com.google.widevine.software.drm.jar\\"/>
                </permissions>"
                                echo -e "$script_text" > $install_partition/etc/permissions/com.google.widevine.software.drm.xml
                                set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.widevine.software.drm.xml"
                                installPath=$product_prefix"etc/permissions/com.google.widevine.software.drm.xml"
                                echo "install=$installPath" >> /tmp/addon/$packagePath
                                if [ -f "$install_partition/etc/permissions/com.google.widevine.software.drm.xml" ]; then
                                  addToLog "- $install_partition/etc/permissions/com.google.widevine.software.drm.xml Successfully Written!"
                                fi"""
        extra_files_go.additional_installer_script += """
                                script_text="<permissions>
                    <library name=\\"com.google.android.media.effects\\"
                            file=\\"$install_partition/framework/com.google.android.media.effects.jar\\" />

                </permissions>"
                                echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.media.effects.xml
                                set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.media.effects.xml"
                                installPath=$product_prefix"etc/permissions/com.google.android.media.effects.xml"
                                echo "install=$installPath" >> /tmp/addon/$packagePath
                                if [ -f "$install_partition/etc/permissions/com.google.android.media.effects.xml" ]; then
                                  addToLog "- $install_partition/etc/permissions/com.google.android.media.effects.xml Successfully Written!"
                                fi"""
        extra_files_go.predefined_file_list.append("etc/sysconfig/google-hiddenapi-package-whitelist.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/pixel_experience_2017.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/pixel_experience_2018.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/pixel_experience_2019_midyear.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/pixel_experience_2019.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/pixel_2019_exclusive.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/nexus.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/google_build.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/google_vr_build.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/google.xml")
        extra_files_go.predefined_file_list.append("framework/com.google.android.maps.jar")
        extra_files_go.predefined_file_list.append("framework/com.google.android.dialer.support.jar")
        extra_files_go.predefined_file_list.append("framework/com.google.widevine.software.drm.jar")
        extra_files_go.predefined_file_list.append("framework/com.google.android.media.effects.jar")
        extra_files_go.predefined_file_list.append("lib64/libgdx.so")
        extra_files_go.predefined_file_list.append("etc/preferred-apps/google_go.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/google_dialergo_experience.xml")
        extra_files_go.predefined_file_list.append("etc/sysconfig/gmsexpress.xml")

        core_go = AppSet("CoreGo")
        core_go.add_package(extra_files_go)

        prebuiltgmscore = Package("PrebuiltGmsCore", "com.google.android.gms", Constants.is_priv_app, "GmsCore")
        prebuiltgmscore.delete_in_rom("PrebuiltGmsCoreQt")
        prebuiltgmscore.delete_in_rom("PrebuiltGmsCoreRvc")
        prebuiltgmscore.delete_in_rom("GmsCore")
        prebuiltgmscore.additional_installer_script = """
        sed -i '/allow-in-power-save package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
        sed -i '/allow-in-data-usage-save package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
        sed -i '/allow-unthrottled-location package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
        sed -i '/allow-ignore-location-settings package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
        addToLog \"- Battery Optimization Done in $install_partition/etc/permissions/*.xml!\"
        sed -i '/allow-in-power-save package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
        sed -i '/allow-in-data-usage-save package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
        sed -i '/allow-unthrottled-location package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
        sed -i '/allow-ignore-location-settings package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
        addToLog \"- Battery Optimization Done in $install_partition/etc/sysconfig/*.xml!\"
                """
        core_go.add_package(prebuiltgmscore)

        phonesky = Package("Phonesky", "com.android.vending", Constants.is_priv_app, "GooglePlayStore")
        core_go.add_package(phonesky)

        googleservicesframework = Package("GoogleServicesFramework", "com.google.android.gsf", Constants.is_priv_app)
        core_go.add_package(googleservicesframework)

        googlecontactssyncadapter = Package("GoogleContactsSyncAdapter", "com.google.android.syncadapters.contacts",
                                            Constants.is_system_app)
        core_go.add_package(googlecontactssyncadapter)

        googlecalendarsync = Package("GoogleCalendarSyncAdapter", "com.google.android.syncadapters.calendar",
                                     Constants.is_system_app)
        core_go.add_package(googlecalendarsync)

        youtube = Package("YouTube", "com.google.android.youtube", Constants.is_system_app)
        core_go.add_package(youtube)

        pixel_launcher_set = NikGappsPackages.get_pixel_launcher()
        for pkg in pixel_launcher_set.package_list:
            core_go.add_package(pkg)
        app_set_list = [core_go]

        google_go = Package("GoogleGo", "com.google.android.apps.searchlite", Constants.is_priv_app)
        app_set_list.append(AppSet("GoogleGo", [google_go]))

        google_assistant_go = Package("AssistantGo", "com.google.android.apps.assistant", Constants.is_priv_app)
        app_set_list.append(AppSet("AssistantGo", [google_assistant_go]))

        google_maps_go = Package("MapsGo", "com.google.android.apps.mapslite", Constants.is_system_app)
        app_set_list.append(AppSet("MapsGo", [google_maps_go]))

        navigation_go = Package("NavigationGo", "com.google.android.apps.navlite", Constants.is_system_app)
        app_set_list.append(AppSet("NavigationGo", [navigation_go]))

        gallery_go = Package("GalleryGo", "com.google.android.apps.photosgo", Constants.is_system_app)
        app_set_list.append(AppSet("GalleryGo", [gallery_go]))

        gmail_go = Package("GmailGo", "com.google.android.gm.lite", Constants.is_system_app)
        app_set_list.append(AppSet("GmailGo", [gmail_go]))

        return app_set_list

    @staticmethod
    def get_core_package():
        files = Package("ExtraFiles", None, None)
        files.predefined_file_list.append("etc/default-permissions/default-permissions.xml")
        if TARGET_ANDROID_VERSION <= 10:
            files.predefined_file_list.append("etc/default-permissions/opengapps-permissions.xml")
        if TARGET_ANDROID_VERSION == 11:
            files.predefined_file_list.append("etc/default-permissions/default-permissions-google.xml")
            files.predefined_file_list.append("etc/default-permissions/nikgapps-permissions.xml")
        if TARGET_ANDROID_VERSION <= 10:
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google.xml")
        files.predefined_file_list.append("etc/permissions/privapp-permissions-hotword.xml")
        if TARGET_ANDROID_VERSION == 9:
            files.predefined_file_list.append("etc/permissions/privapp-permissions-elgoog.xml")
        if TARGET_ANDROID_VERSION == 10:
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google-p.xml")
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google-ps.xml")
            files.predefined_file_list.append("etc/permissions/split-permissions-google.xml")
        if TARGET_ANDROID_VERSION == 11:
            files.predefined_file_list.append("etc/permissions/com.google.android.dialer.support.xml")
            files.predefined_file_list.append("etc/permissions/NikGapps-privapp-permissions-google.xml")
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google-comms-suite.xml")
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google-p.xml")
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google-product.xml")
            files.predefined_file_list.append("etc/permissions/privapp-permissions-google-system-ext.xml")
            files.predefined_file_list.append("etc/permissions/split-permissions-google.xml")
        files.additional_installer_script = """script_text="<permissions>
                    <!-- Shared library required on the device to get Google Dialer updates from
                         Play Store. This will be deprecated once Google Dialer play store
                         updates stop supporting pre-O devices. -->
                    <library name=\\"com.google.android.dialer.support\\"
                      file=\\"$install_partition/framework/com.google.android.dialer.support.jar\\" />

                    <!-- Starting from Android O and above, this system feature is required for
                         getting Google Dialer play store updates. -->
                    <feature name=\\"com.google.android.apps.dialer.SUPPORTED\\" />
                </permissions>"
                echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.dialer.support.xml
                set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.dialer.support.xml"
                installPath=$product_prefix"etc/permissions/com.google.android.dialer.support.xml"
                echo "install=$installPath" >> /tmp/addon/$packagePath
                if [ -f "$install_partition/etc/permissions/com.google.android.dialer.support.xml" ]; then
                  addToLog "- $install_partition/etc/permissions/com.google.android.dialer.support.xml Successfully Written!"
                fi"""
        files.additional_installer_script += """
                script_text="<permissions>
                    <library name=\\"com.google.android.maps\\"
                            file=\\"$install_partition/framework/com.google.android.maps.jar\\" />
                </permissions>"
                echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.maps.xml
                set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.maps.xml"
                installPath=$product_prefix"etc/permissions/com.google.android.maps.xml"
                echo "install=$installPath" >> /tmp/addon/$packagePath
                if [ -f "$install_partition/etc/permissions/com.google.android.maps.xml" ]; then
                  addToLog "- $install_partition/etc/permissions/com.google.android.maps.xml Successfully Written!"
                fi"""
        files.additional_installer_script += """
                        script_text="<permissions>
            <library name=\\"com.google.widevine.software.drm\\"
                file=\\"/system/product/framework/com.google.widevine.software.drm.jar\\"/>
        </permissions>"
                        echo -e "$script_text" > $install_partition/etc/permissions/com.google.widevine.software.drm.xml
                        set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.widevine.software.drm.xml"
                        installPath=$product_prefix"etc/permissions/com.google.widevine.software.drm.xml"
                        echo "install=$installPath" >> /tmp/addon/$packagePath
                        if [ -f "$install_partition/etc/permissions/com.google.widevine.software.drm.xml" ]; then
                          addToLog "- $install_partition/etc/permissions/com.google.widevine.software.drm.xml Successfully Written!"
                        fi"""
        files.additional_installer_script += """
                        script_text="<permissions>
            <library name=\\"com.google.android.media.effects\\"
                    file=\\"$install_partition/framework/com.google.android.media.effects.jar\\" />

        </permissions>"
                        echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.media.effects.xml
                        set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.media.effects.xml"
                        installPath=$product_prefix"etc/permissions/com.google.android.media.effects.xml"
                        echo "install=$installPath" >> /tmp/addon/$packagePath
                        if [ -f "$install_partition/etc/permissions/com.google.android.media.effects.xml" ]; then
                          addToLog "- $install_partition/etc/permissions/com.google.android.media.effects.xml Successfully Written!"
                        fi"""
        if TARGET_ANDROID_VERSION <= 10:
            files.predefined_file_list.append("etc/sysconfig/google_build.xml")
            files.predefined_file_list.append("etc/sysconfig/google_vr_build.xml")
            files.predefined_file_list.append("etc/sysconfig/google.xml")
        if TARGET_ANDROID_VERSION == 11:
            files.predefined_file_list.append("etc/sysconfig/backup.xml")
            files.predefined_file_list.append("etc/sysconfig/dialer_experience.xml")
            files.predefined_file_list.append("etc/sysconfig/pixel.xml")
            files.predefined_file_list.append("etc/sysconfig/preinstalled-packages-platform-handheld-product.xml")
            files.predefined_file_list.append("etc/sysconfig/preinstalled-packages-platform-overlays.xml")
            files.predefined_file_list.append("etc/sysconfig/wellbeing.xml")
        files.predefined_file_list.append("etc/sysconfig/google-hiddenapi-package-whitelist.xml")
        files.predefined_file_list.append("etc/sysconfig/pixel_experience_2017.xml")
        files.predefined_file_list.append("etc/sysconfig/pixel_experience_2018.xml")
        files.predefined_file_list.append("etc/sysconfig/pixel_experience_2019_midyear.xml")
        files.predefined_file_list.append("etc/sysconfig/pixel_experience_2019.xml")
        files.predefined_file_list.append("etc/sysconfig/pixel_2019_exclusive.xml")
        files.predefined_file_list.append("etc/sysconfig/nexus.xml")
        files.predefined_file_list.append("framework/com.google.android.maps.jar")
        files.predefined_file_list.append("framework/com.google.android.dialer.support.jar")
        files.predefined_file_list.append("framework/com.google.widevine.software.drm.jar")
        files.predefined_file_list.append("framework/com.google.android.media.effects.jar")
        files.predefined_file_list.append("lib64/libgdx.so")
        prebuiltgmscore = Package("PrebuiltGmsCore", "com.google.android.gms", Constants.is_priv_app, "GmsCore")
        prebuiltgmscore.delete_in_rom("PrebuiltGmsCoreQt")
        prebuiltgmscore.delete_in_rom("PrebuiltGmsCoreRvc")
        prebuiltgmscore.delete_in_rom("GmsCore")
        prebuiltgmscore.additional_installer_script = """
sed -i '/allow-in-power-save package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
sed -i '/allow-in-data-usage-save package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
sed -i '/allow-unthrottled-location package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
sed -i '/allow-ignore-location-settings package=\"com.google.android.gms\"/d' $install_partition/etc/permissions/*.xml
addToLog \"- Battery Optimization Done in $install_partition/etc/permissions/*.xml!\"
sed -i '/allow-in-power-save package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
sed -i '/allow-in-data-usage-save package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
sed -i '/allow-unthrottled-location package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
sed -i '/allow-ignore-location-settings package=\"com.google.android.gms\"/d' $install_partition/etc/sysconfig/*.xml
addToLog \"- Battery Optimization Done in $install_partition/etc/sysconfig/*.xml!\"
        """
        phonesky = Package("Phonesky", "com.android.vending", Constants.is_priv_app, "GooglePlayStore")
        googleservicesframework = Package("GoogleServicesFramework", "com.google.android.gsf", Constants.is_priv_app)
        googlecontactssyncadapter = Package("GoogleContactsSyncAdapter", "com.google.android.syncadapters.contacts",
                                            Constants.is_system_app)
        googlecalendarsync = Package("GoogleCalendarSyncAdapter", "com.google.android.syncadapters.calendar",
                                     Constants.is_system_app)
        gapps_list = [files, phonesky, googleservicesframework, googlecontactssyncadapter, googlecalendarsync,
                      prebuiltgmscore]
        return [AppSet("Core", gapps_list)]

    @staticmethod
    def get_basic_package():
        app_set_list = NikGappsPackages.get_core_package()
        digital_wellbeing = Package("WellbeingPreBuilt", "com.google.android.apps.wellbeing", Constants.is_priv_app,
                                    "DigitalWellbeing")
        if TARGET_ANDROID_VERSION == 10 and ADB_ROOT_ENABLED:
            digital_wellbeing.predefined_file_list.append("overlay/WellbeingOverlay.apk")
        vanced_manager = Package("VancedManager", "com.vanced.manager", Constants.is_system_app)
        vanced_manager.enabled = 0
        app_set_list.append(AppSet("DigitalWellbeing", [digital_wellbeing]))
        app_set_list.append(AppSet("VancedManager", [vanced_manager]))
        google_messages = Package("PrebuiltBugle", "com.google.android.apps.messaging", Constants.is_system_app,
                                  "GoogleMessages")
        google_messages.delete("RevengeMessages")
        google_messages.delete("messaging")
        google_messages.delete("Messaging")
        google_messages.delete("QKSMS")
        google_messages.delete("Mms")
        app_set_list.append(AppSet("GoogleMessages", [google_messages]))

        google_dialer = Package("GoogleDialer", "com.google.android.dialer", Constants.is_priv_app)
        if TARGET_ANDROID_VERSION == 10 and ADB_ROOT_ENABLED:
            google_dialer.predefined_file_list.append("overlay/PhoneOverlay.apk")
            google_dialer.predefined_file_list.append("overlay/TelecomOverlay.apk")
            google_dialer.predefined_file_list.append("overlay/DefaultDialerOverlay.apk")
        google_dialer.predefined_file_list.append("framework/com.google.android.dialer.support.jar")
        google_dialer.delete("Dialer")
        google_dialer.additional_installer_script = """script_text="<permissions>
                            <!-- Shared library required on the device to get Google Dialer updates from
                                 Play Store. This will be deprecated once Google Dialer play store
                                 updates stop supporting pre-O devices. -->
                            <library name=\\"com.google.android.dialer.support\\"
                              file=\\"$install_partition/framework/com.google.android.dialer.support.jar\\" />

                            <!-- Starting from Android O and above, this system feature is required for
                                 getting Google Dialer play store updates. -->
                            <feature name=\\"com.google.android.apps.dialer.SUPPORTED\\" />
                        </permissions>"
                        echo -e "$script_text" > $install_partition/etc/permissions/com.google.android.dialer.support.xml
                        set_perm 0 0 0644 "$install_partition/etc/permissions/com.google.android.dialer.support.xml"
                        installPath=$product_prefix"etc/permissions/com.google.android.dialer.support.xml"
                        echo "install=$installPath" >> /tmp/addon/$packagePath
                        if [ -f "$install_partition/etc/permissions/com.google.android.dialer.support.xml" ]; then
                          addToLog "- $install_partition/etc/permissions/com.google.android.dialer.support.xml Successfully Written!"
                        fi

                         # set Google Dialer as default; based on the work of osm0sis @ xda-developers
                          setver=\"122\"  # lowest version in MM, tagged at 6.0.0
                          setsec=\"/data/system/users/0/settings_secure.xml\"
                          if [ -f \"$setsec\" ]; then
                            if grep -q 'dialer_default_application' \"$setsec\"; then
                              if ! grep -q 'dialer_default_application\" value=\"com.google.android.dialer' \"$setsec\"; then
                                curentry=\"$(grep -o 'dialer_default_application\" value=.*$' \"$setsec\")\"
                                newentry='dialer_default_application\" value=\"com.google.android.dialer\" package=\"android\" />\\r'
                                sed -i \"s;${curentry};${newentry};\" \"$setsec\"
                              fi
                            else
                              max=\"0\"
                              for i in $(grep -o 'id=.*$' \"$setsec\" | cut -d '\"' -f 2); do
                                test \"$i\" -gt \"$max\" && max=\"$i\"
                              done
                              entry='<setting id=\"'\"$((max + 1))\"'\" name=\"dialer_default_application\" value=\"com.google.android.dialer\" package=\"android\" />\\r'
                              sed -i \"/<settings version=\\\"/a\ \ ${entry}\" \"$setsec\"
                            fi
                          else
                            if [ ! -d \"/data/system/users/0\" ]; then
                              install -d \"/data/system/users/0\"
                              chown -R 1000:1000 \"/data/system\"
                              chmod -R 775 \"/data/system\"
                              chmod 700 \"/data/system/users/0\"
                            fi
                            { echo -e \"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\\r\"
                            echo -e '<settings version=\"'$setver'\">\\r'
                            echo -e '  <setting id="1" name=\"dialer_default_application\" value=\"com.google.android.dialer\" package=\"android\" />\\r'
                            echo -e '</settings>'; } > \"$setsec\"
                          fi
                          chown 1000:1000 \"$setsec\"
                          chmod 600 \"$setsec\"

                          if [ -f "$setsec" ]; then
                            addToLog "- $setsec Successfully Written!"
                          fi"""
        app_set_list.append(AppSet("GoogleDialer", [google_dialer]))

        google_contacts = Package("GoogleContacts", "com.google.android.contacts", Constants.is_priv_app)
        google_contacts.delete("Contacts")
        app_set_list.append(AppSet("GoogleContacts", [google_contacts]))

        carrier_services = Package("CarrierServices", "com.google.android.ims", Constants.is_priv_app)
        app_set_list.append(AppSet("CarrierServices", [carrier_services]))
        google_clock = Package("PrebuiltDeskClockGoogle", "com.google.android.deskclock", Constants.is_system_app,
                               "GoogleClock")
        google_clock.delete("DeskClock")
        app_set_list.append(AppSet("GoogleClock", [google_clock]))
        return app_set_list

    @staticmethod
    def get_omni_package():
        app_set_list = NikGappsPackages.get_basic_package()
        app_set_list.append(NikGappsPackages.get_setup_wizard())
        if TARGET_ANDROID_VERSION >= 10:
            app_set_list.append(NikGappsPackages.get_pixelize_set())
        calculator = Package("CalculatorGooglePrebuilt", "com.google.android.calculator", Constants.is_system_app,
                             "GoogleCalculator")
        calculator.delete("ExactCalculator")
        calculator.delete("RevengeOSCalculator")
        app_set_list.append(AppSet("GoogleCalculator", [calculator]))
        google_drive = Package("Drive", "com.google.android.apps.docs", Constants.is_system_app)
        app_set_list.append(AppSet("Drive", [google_drive]))
        google_maps = Package("GoogleMaps", "com.google.android.apps.maps", Constants.is_priv_app)
        google_maps.delete_in_rom("Maps")
        app_set_list.append(AppSet("GoogleMaps", [google_maps]))
        if TARGET_ANDROID_VERSION == 11:
            google_location_history = Package("LocationHistoryPrebuilt", "com.google.android.gms.location.history",
                                              Constants.is_system_app, "GoogleLocationHistory")
            google_location_history.delete_in_rom("LocationHistoryPrebuilt")
            app_set_list.append(AppSet("GoogleLocationHistory", [google_location_history]))
        gmail = Package("PrebuiltGmail", "com.google.android.gm", Constants.is_system_app, "Gmail")
        gmail.delete("Email")
        gmail.delete("PrebuiltEmailGoogle")
        app_set_list.append(AppSet("Gmail", [gmail]))
        google_photos = Package("Photos", "com.google.android.apps.photos", Constants.is_system_app, "GooglePhotos")
        google_photos.delete("Gallery")
        google_photos.delete("SimpleGallery")
        google_photos.delete("Gallery2")
        google_photos.delete("MotGallery")
        google_photos.delete("MediaShortcuts")
        google_photos.delete("SimpleGallery")
        google_photos.delete("FineOSGallery")
        google_photos.delete("GalleryX")
        google_photos.delete("MiuiGallery")
        google_photos.delete("SnapdragonGallery")
        app_set_list.append(AppSet("GooglePhotos", [google_photos]))
        google_turbo = Package("Turbo", "com.google.android.apps.turbo", Constants.is_priv_app, "DeviceHealthServices")
        google_turbo.delete_in_rom("TurboPrebuilt")
        app_set_list.append(AppSet("DeviceHealthServices", [google_turbo]))
        flipendo = Package("Flipendo", "com.google.android.flipendo", Constants.is_system_app)
        app_set_list.append(AppSet("Flipendo", [flipendo]))
        return app_set_list

    @staticmethod
    def get_stock_package():
        app_set_list = NikGappsPackages.get_omni_package()
        google_velvet = Package("Velvet", "com.google.android.googlequicksearchbox", Constants.is_priv_app)
        google_velvet.priv_app_permissions.append("android.permission.WRITE_APN_SETTINGS")
        google_velvet.priv_app_permissions.append("android.permission.BLUETOOTH_PRIVILEGED")
        google_velvet.additional_installer_script = """
                set_prop "ro.opa.eligible_device" "true" "$install_partition/build.prop"
                        """
        app_set_list.append(AppSet("Velvet", [google_velvet]))
        google_board = Package("LatinIMEGooglePrebuilt", "com.google.android.inputmethod.latin",
                               Constants.is_system_app, "GBoard")
        google_board.additional_installer_script = """
                set_prop "ro.com.google.ime.bs_theme" "true" "$install_partition/build.prop"
                set_prop "ro.com.google.ime.theme_id" "5" "$install_partition/build.prop"
                set_prop "ro.com.google.ime.system_lm_dir" "$install_partition/usr/share/ime/google/d3_lms" "$install_partition/build.prop"
        """
        google_board.delete("LatinIME")
        app_set_list.append(AppSet("GBoard", [google_board]))
        app_set_list.append(NikGappsPackages.get_pixel_launcher())
        if TARGET_ANDROID_VERSION == 11:
            app_set_list.append(NikGappsPackages.get_google_files())
        play_games = Package("PlayGames", "com.google.android.play.games", Constants.is_system_app)
        app_set_list.append(AppSet("PlayGames", [play_games]))
        google_calendar = Package("CalendarGooglePrebuilt", "com.google.android.calendar", Constants.is_priv_app,
                                  "GoogleCalendar")
        google_calendar.delete("Calendar")
        google_calendar.delete("Etar")
        google_calendar.delete("SimpleCalendar")
        app_set_list.append(AppSet("GoogleCalendar", [google_calendar]))
        google_markup = Package("MarkupGoogle", "com.google.android.markup", Constants.is_system_app)
        app_set_list.append(AppSet("MarkupGoogle", [google_markup]))
        google_wallpaper = Package("WallpaperPickerGooglePrebuilt", "com.google.android.apps.wallpaper",
                                   Constants.is_priv_app, "GoogleWallpaper")
        app_set_list.append(AppSet("GoogleWallpaper", [google_wallpaper]))
        google_feedback = Package("GoogleFeedback", "com.google.android.feedback", Constants.is_priv_app)
        app_set_list.append(AppSet("GoogleFeedback", [google_feedback]))
        google_partner_setup = Package("PartnerSetupPrebuilt", "com.google.android.partnersetup", Constants.is_priv_app,
                                       "GooglePartnerSetup")
        app_set_list.append(AppSet("GooglePartnerSetup", [google_partner_setup]))
        google_sounds = Package("SoundPickerPrebuilt", "com.google.android.soundpicker", Constants.is_system_app,
                                "GoogleSounds")
        app_set_list.append(AppSet("GoogleSounds", [google_sounds]))
        if TARGET_ANDROID_VERSION >= 10:
            android_device_policy = Package("DevicePolicyPrebuilt", "com.google.android.apps.work.clouddpc",
                                            Constants.is_system_app, "AndroidDevicePolicy")
            app_set_list.append(AppSet("AndroidDevicePolicy", [android_device_policy]))
        return app_set_list

    @staticmethod
    def get_full_package():
        app_set_list = NikGappsPackages.get_stock_package()
        google_keep = Package("PrebuiltKeep", "com.google.android.keep", Constants.is_priv_app, "GoogleKeep")
        app_set_list.append(AppSet("GoogleKeep", [google_keep]))
        google_play_books = Package("Books", "com.google.android.apps.books", Constants.is_system_app)
        app_set_list.append(AppSet("Books", [google_play_books]))
        google_assistant = Package("Assistant", "com.google.android.apps.googleassistant", Constants.is_priv_app)
        app_set_list.append(AppSet("Assistant", [google_assistant]))
        youtube_music = Package("YouTubeMusicPrebuilt", "com.google.android.apps.youtube.music",
                                Constants.is_system_app,
                                "YouTubeMusic")
        youtube_music.delete("SnapdragonMusic")
        youtube_music.delete("GooglePlayMusic")
        app_set_list.append(AppSet("YouTubeMusic", [youtube_music]))
        google_recorder = Package("RecorderPrebuilt", "com.google.android.apps.recorder", Constants.is_priv_app,
                                  "GoogleRecorder")
        google_recorder.delete("QtiSoundRecorder")
        app_set_list.append(AppSet("GoogleRecorder", [google_recorder]))
        google_tts = Package("GoogleTTS", "com.google.android.tts", Constants.is_system_app)
        google_tts.delete("PicoTts")
        app_set_list.append(AppSet("GoogleTTS", [google_tts]))
        talkback = Package("talkback", "com.google.android.marvin.talkback", Constants.is_system_app, "GoogleTalkback")
        google_talkback = AppSet("GoogleTalkback", [talkback])
        app_set_list.append(google_talkback)
        if TARGET_ANDROID_VERSION >= 10:
            google_device_setup = Package("OTAConfigPrebuilt", "com.google.android.apps.work.oobconfig",
                                          Constants.is_priv_app, "DeviceSetup")
            app_set_list.append(AppSet("DeviceSetup", [google_device_setup]))
        android_auto = Package("AndroidAutoStubPrebuilt", "com.google.android.projection.gearhead",
                               Constants.is_priv_app, "AndroidAuto")
        app_set_list.append(AppSet("AndroidAuto", [android_auto]))
        app_set_list.append(NikGappsPackages.get_chrome())
        return app_set_list

    @staticmethod
    def get_google_files():
        google_files = Package("FilesPrebuilt", "com.google.android.apps.nbu.files", Constants.is_priv_app,
                               "GoogleFiles")
        google_files.predefined_file_list.append("overlay/FilesOverlay/FilesOverlay.apk")
        google_files.predefined_file_list.append(
            "overlay/PixelDocumentsUIGoogleOverlay/PixelDocumentsUIGoogleOverlay.apk")
        storage_manager_google = Package("StorageManagerGoogle", "com.google.android.storagemanager",
                                         Constants.is_priv_app, "StorageManager")
        app_set_list = AppSet("GoogleFiles", [google_files, storage_manager_google])
        return app_set_list

    @staticmethod
    def get_chrome():
        google_chrome = Package("GoogleChrome", "com.android.chrome", Constants.is_priv_app)
        google_chrome.delete("Bolt")
        google_chrome.delete("Browser")
        google_chrome.delete("Browser2")
        google_chrome.delete("BrowserIntl")
        google_chrome.delete("BrowserProviderProxy")
        google_chrome.delete("Chromium")
        google_chrome.delete("DuckDuckGo")
        google_chrome.delete("Fluxion")
        google_chrome.delete("Gello")
        google_chrome.delete("Jelly")
        google_chrome.delete("PA_Browser")
        google_chrome.delete("PABrowser")
        google_chrome.delete("YuBrowser")
        google_chrome.delete("BLUOpera")
        google_chrome.delete("BLUOperaPreinstall")
        google_chrome.delete("ViaBrowser")
        app_set_list = AppSet("GoogleChrome")
        app_set_list.add_package(google_chrome)
        if TARGET_ANDROID_VERSION >= 10:
            google_webview = Package("WebViewGoogle", "com.google.android.webview", Constants.is_system_app)
            google_webview.predefined_file_list.append("overlay/GoogleWebViewOverlay.apk")
            google_webview.delete("webview")
            trichromelibrary = Package("TrichromeLibrary", "com.google.android.trichromelibrary", Constants.is_system_app)
            app_set_list.add_package(google_webview)
            app_set_list.add_package(trichromelibrary)
        return app_set_list

    @staticmethod
    def get_setup_wizard():
        setup_wizard = Package("SetupWizardPrebuilt", "com.google.android.setupwizard", Constants.is_priv_app,
                               "SetupWizard")
        setup_wizard.delete("Provision")
        setup_wizard.delete("SetupWizardPrebuilt")
        setup_wizard.delete("SetupWizard")
        setup_wizard.delete("GoogleRestore")
        setup_wizard.additional_installer_script = """
set_prop "setupwizard.feature.baseline_setupwizard_enabled" "true" "$install_partition/build.prop"
set_prop "ro.setupwizard.enterprise_mode" "1" "$install_partition/build.prop"
set_prop "ro.setupwizard.rotation_locked" "true" "$install_partition/build.prop"
set_prop "setupwizard.enable_assist_gesture_training" "true" "$install_partition/build.prop"
set_prop "setupwizard.theme" "glif_v3_light" "$install_partition/build.prop"
set_prop "setupwizard.feature.skip_button_use_mobile_data.carrier1839" "true" "$install_partition/build.prop"
set_prop "setupwizard.feature.show_pai_screen_in_main_flow.carrier1839" "false" "$install_partition/build.prop"
set_prop "setupwizard.feature.show_pixel_tos" "false" "$install_partition/build.prop"
        """
        google_restore = Package("GoogleRestore", "com.google.android.apps.restore", Constants.is_priv_app)
        setup_wizard_set = AppSet("SetupWizard")
        setup_wizard_set.add_package(setup_wizard)
        setup_wizard_set.add_package(google_restore)
        if TARGET_ANDROID_VERSION >= 10:
            google_one_time_initializer = Package("GoogleOneTimeInitializer", "com.google.android.onetimeinitializer",
                                                  Constants.is_priv_app)
            setup_wizard_set.add_package(google_one_time_initializer)
        return setup_wizard_set

    @staticmethod
    def get_pixelize_set():
        pixel_setup_wizard_overlay = Package("PixelSetupWizardOverlay", "com.google.android.pixel.setupwizard.overlay",
                                             Constants.is_system_app)
        pixel_setup_wizard_aod_overlay = Package("PixelSetupWizardAodOverlay",
                                                 "com.google.android.pixel.setupwizard.overlay.aod",
                                                 Constants.is_system_app)
        pixel_setup_wizard = Package("PixelSetupWizard", "com.google.android.pixel.setupwizard", Constants.is_priv_app)
        android_migrate_prebuilt = Package("AndroidMigratePrebuilt", "com.google.android.apps.pixelmigrate",
                                           Constants.is_priv_app)
        pixel_tips = Package("TipsPrebuilt", "com.google.android.apps.tips", Constants.is_priv_app, "PixelTips")
        pixel_config_overlays = Package("PixelConfigOverlays", None, None)
        pixel_config_overlays.predefined_file_list.append(
            "overlay/IconPackRoundedPixelLauncher/IconPackRoundedPixelLauncherOverlay.apk")
        pixel_config_overlays.predefined_file_list.append(
            "overlay/IconPackFilledPixelLauncher/IconPackFilledPixelLauncherOverlay.apk")
        pixel_config_overlays.predefined_file_list.append(
            "overlay/IconPackCircularPixelLauncher/IconPackCircularPixelLauncherOverlay.apk")
        pixel_config_overlays.predefined_file_list.append("overlay/PixelConfigOverlay2018.apk")
        pixel_config_overlays.predefined_file_list.append("overlay/PixelConfigOverlay2019.apk")
        pixel_config_overlays.predefined_file_list.append("overlay/PixelConfigOverlay2019Midyear.apk")
        pixel_config_overlays.predefined_file_list.append("overlay/PixelConfigOverlaySunfish.apk")
        pixelize_set = AppSet("Pixelize")
        if TARGET_ANDROID_VERSION == 10:
            pixelize_set.add_package(pixel_setup_wizard_overlay)
            pixelize_set.add_package(pixel_setup_wizard_aod_overlay)
        if TARGET_ANDROID_VERSION >= 10:
            pixelize_set.add_package(pixel_setup_wizard)
            pixelize_set.add_package(android_migrate_prebuilt)
            pixelize_set.add_package(pixel_tips)
        if TARGET_ANDROID_VERSION == 11:
            pixelize_set.add_package(pixel_config_overlays)
        return pixelize_set

    @staticmethod
    def get_pixel_launcher():
        pixel_launcher = Package("NexusLauncherPrebuilt", "com.google.android.apps.nexuslauncher",
                                 Constants.is_priv_app, "PixelLauncher")
        pixel_launcher.priv_app_permissions.append("android.permission.PACKAGE_USAGE_STATS")
        pixel_launcher.delete("TrebuchetQuickStep")
        # pixel_launcher.delete("Launcher3QuickStep")
        if TARGET_ANDROID_VERSION <= 10:
            pixel_launcher.predefined_file_list.append("overlay/PixelLauncherOverlay.apk")
        if TARGET_ANDROID_VERSION == 11:
            pixel_launcher.predefined_file_list.append("overlay/PixelConfigOverlayCommon.apk")
            pixel_launcher.predefined_file_list.append("etc/permissions/com.android.launcher3.xml")
            pixel_launcher.predefined_file_list.append(
                "etc/sysconfig/hiddenapi-whitelist-com.google.android.apps.nexuslauncher.xml")
            pixel_launcher.predefined_file_list.append(
                "etc/permissions/privapp-permissions-com.google.android.apps.nexuslauncher.xml")
        device_personalization_services = Package("MatchmakerPrebuiltPixel4", "com.google.android.as",
                                                  Constants.is_priv_app, "DevicePersonalizationServices")
        gapps_list = [pixel_launcher]
        if TARGET_ANDROID_VERSION >= 9:
            if ADB_ROOT_ENABLED and TARGET_ANDROID_VERSION == 10:
                device_personalization_services.predefined_file_list.append(
                    "overlay/DevicePersonalizationServicesConfig.apk")
            device_personalization_services.delete_in_rom("DevicePersonalizationPrebuiltPixel4")
            gapps_list.append(device_personalization_services)
        if TARGET_ANDROID_VERSION == 11:
            quick_access_wallet = Package("QuickAccessWallet", "com.android.systemui.plugin.globalactions.wallet",
                                          Constants.is_priv_app)
            gapps_list.append(quick_access_wallet)
        return AppSet("PixelLauncher", gapps_list)

    @staticmethod
    def get_lawnchair():
        lawnchair_set = AppSet("Lawnchair")
        from Config import TARGET_ANDROID_VERSION
        if TARGET_ANDROID_VERSION == 10:
            lawnchair_ci = Package("Lawnchair", "ch.deletescape.lawnchair.ci", Constants.is_priv_app)
            lawnchair_ci.delete("Lawnchair")
            lawnchair_ci.delete("Lawnfeed")
            if "etc/permissions/privapp-permissions-lawnchair.xml" not in lawnchair_ci.predefined_file_list:
                lawnchair_ci.predefined_file_list.append("etc/permissions/privapp-permissions-lawnchair.xml")
            if "etc/sysconfig/lawnchair-hiddenapi-package-whitelist.xml" not in lawnchair_ci.predefined_file_list:
                lawnchair_ci.predefined_file_list.append("etc/sysconfig/lawnchair-hiddenapi-package-whitelist.xml")
            overlay = "overlay/LawnchairRecentsProvider/LawnchairRecentsProvider.apk"
            lawnchair_recents_provider = Package("LawnchairRecentsProvider", "com.android.overlay.shady.recents", None)
            if overlay not in lawnchair_recents_provider.predefined_file_list:
                lawnchair_recents_provider.predefined_file_list.append(overlay)
            lawnchair_set.add_package(lawnchair_ci)
            lawnchair_recents_provider.enabled = 0
            lawnchair_set.add_package(lawnchair_recents_provider)
        else:
            lawnchair = Package("Lawnchair", "ch.deletescape.lawnchair.plah", Constants.is_priv_app)
            lawnchair.delete("Lawnchair")
            lawnchair.delete("Lawnfeed")
            lawnchair_set.add_package(lawnchair)
        lawnfeed = Package("Lawnfeed", "ch.deletescape.lawnchair.lawnfeed", Constants.is_system_app)
        lawnchair_set.add_package(lawnfeed)
        return lawnchair_set
