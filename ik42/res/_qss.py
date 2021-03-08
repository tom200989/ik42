"""
本类为QSS样式引用表
"""

class QSS:  # 类名不要以下划线开头

    # 窗口背景
    background_all = """
    * {
        background-color: #2D2D2D;
    }
    """

    # 成功状态
    iv_ik42_success = """
    * {
        border-image:url(:/ik42/ik42_success.png)
    }
    """

    # 失败状态
    iv_ik42_error = """
    * {
        border-image:url(:/ik42/ik42_error.png)
    }
    """

    # 超时状态
    iv_ik42_timeout = """
    * {
        border-image:url(:/ik42/ik42_timeout.png)
    }
    """

    # 状态点击按钮
    bt_ik42_ok_try_again = """
    * {
        background-color:#515151;
        border-radius:15px;
        font-family:微软雅黑;
        font-size:14px;
        color:white;
    }
    
    * :hover{
        background-color:#a4a4a4;
    }
    
    * :pressed{
        background-color:#a4a4a4;
    }
    """

    # 状态提示
    tv_ik42_state = """
    * {
        font-family:微软雅黑;
        font-size:14px;
        color:#FFFFFF;
    }
    """

    # U盘
    iv_ik42_u_pan = """
    * {
        border-image:url(:/ik42/ik42_u_pan.png)
    }
    """

    # 认证按钮
    bt_ik42_verify = """
    * {
        border-image:url(:/ik42/ik42_next.png)
    }
    
    * :hover{
        border-image:url(:/ik42/ik42_next_hover.png)
    }
    
    * :pressed{
        border-image:url(:/ik42/ik42_next_hover.png)
    }
    """

    # IK42字体
    tv_ik42_logo = """
    * {
        font-family:微软雅黑;
        font-size:32px;
        color:#BFBFBF;
    }
    """

    # 下拉选择框样式
    cb_ik42_imei = """
    * {
        background-color: #2D2D2D;
        padding-left: 10px;
        font-family: 微软雅黑;
        font-size: 14px;
        color: #FFFFFF;
        border-style: solid;
        border-width: 2px;
        border-color: #ADADAD;
    }
    
    * :disabled{
        background-color: #2D2D2D;
        padding-left: 10px;
        font-family: 微软雅黑;
        font-size: 14px;
        color: #6A6A6A;
        border-style: solid;
        border-width: 2px;
        border-color: #6A6A6A;
    }
    
    * :enabled{
        background-color: #2D2D2D;
        padding-left: 10px;
        font-family: 微软雅黑;
        font-size: 14px;
        color: #FFFFFF;
        border-style: solid;
        border-width: 2px;
        border-color: #ADADAD;
    }
    
    QScrollBar:vertical {
      border: 20px solid red;
      width: 0px;
    }
    
    * :focus{
        border-color: #ADADAD;
    }
    
    * QAbstractItemView{
        outline:0px;
        selection-background-color: #747474;
    }
    
    * QAbstractItemView::item{
        height: 40px;
        background-color: #2D2D2D;
        selection-color:white;
    }
    
    *::drop-down{
        subcontrol-origin: padding;
        subcontrol-position: right center;
        padding-right: 10px;
        border: None;
        width: 20px;
        height: 20px;
    }

    *::down-arrow{
        border-image: url(:/ik42/ik42_pull_arrow.png);
    }
    
    *::down-arrow:on{
        border-image: url(:/ik42/ik42_pull_arrow_pressed.png);
    }
    """

    # 版权
    tv_ik42_copr = """
    * {
        font-family:微软雅黑;
        font-size:12px;
        color:#4A4A4A;
    }
    """

    # 提示
    tv_ik42_tip = """
    * {
        font-family:微软雅黑;
        font-size:12px;
        color:#8F5959;
    }
    """

    # 关闭
    tv_ik42_close = """
    * {
        font-family:微软雅黑;
        font-size:24px;
        color:#ADADAD;
    }
    
    * :hover{
        font-family:微软雅黑;
        font-size:24px;
        color:#FFFFFF;
    }
    
    * :pressed{
        font-family:微软雅黑;
        font-size:24px;
        color:#FFFFFF;
    }
    """

    # 回退
    iv_ik42_back = """
    * {
        border-image:url(:/ik42/ik42_back.png)
    }
    
    * :hover{
        border-image:url(:/ik42/ik42_back_pressed.png)
    }
    
    * :pressed{
        border-image:url(:/ik42/ik42_back_pressed.png)
    }
    """
