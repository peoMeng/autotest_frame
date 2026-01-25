from util.setter import argsetter
from util.common_service import platform_mapper


@platform_mapper(argsetter.test_platform, default_key="default")
class AndroidElement:
    """android UI元素"""
    video = {'OPPO': 'OPPO 视频',
             'default': '视频'}
    music = '音乐'
    soft_store = '软件商店'
    theme_store = '主题商店'
    setting = '设置'
    tool = '工具'
    file_manager = '文件管理'
    recommend = '推荐'
    music_lib = '乐库'
    game = '游戏'
    typeface = '字体'
    setting_search = '搜索设置项'
    file = '文件'
    available_network = '可用网络'
    # 便捷栏
    conv_bar_setting_id = 'id=com.android.systemui:id/settings_button'
    conv_bar_WLAN_expand_id = 'id=com.android.systemui:id/expand_indicator'

    appcenter_collect = {'OPPO': [('video', 'recommend'), ('music', 'music_lib'), ('soft_store', 'game'),
                                  ('theme_store', 'typeface'), ('setting', 'setting_search'), ('file_manager', 'file')]}
