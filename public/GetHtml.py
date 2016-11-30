# -*- coding: utf-8 -*-
__author__ = 'joko'

"""
@author:joko
@time: 16/11/8 下午2:52
"""
import lib.Utils as U


def get_html_tr(case_id, passing_state, img_path, per, device_log, filter_log):
    """

    :param case_id:编号
    :param passing_state: 文本
    :param img_path:图片地址
    :return: html tr部分
    """
    tr = """
    <tr bgcolor="MintCream">
            %(case_id)s
            %(pass)s
            %(img)s
            %(per)s
            %(device_log)s
            %(filter_log)s
    </tr>
    """

    case_id = '<td>{}</td>'.format(case_id)
    passing_state = '<td>{}</td>'.format(passing_state)
    img = '<td><img src="{}" align="absmiddle" width="130" height="200"/></td>'.format(img_path)
    per = '<td><img src="{}" align="absmiddle" width="250" height="200"/></td>'.format(per)
    device_log = '<td><a href="{}">device_log</a></td>'.format(device_log)
    filter_log = '<td><a href="{}">device_filter_log</a></td>'.format(filter_log)

    result = {'case_id': case_id, 'pass': passing_state, 'img': img, 'per': per, 'device_log': device_log,
              'filter_log': filter_log}
    return tr % result


@U.l()
def get_html(log, device, app_info, test_status, result_path):
    """

    :param log: 测试报告报表
    :param device: device信息
    :param app_info: 测试应用信息
    :param test_status: 测试用例信息
    :param result_path: 输出文件夹
    :return:
    """
    all_case, passed, failed = test_status
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <title>Test Report</title>
    </head>
    <body>
    <span style="color:green;"><h1>Test Report</h1></span>
    <p>End Time:{Time}</p>
    <p>{device}</p>
    <p>{app_info}</p>
    <p><span style="color:blue;">All_Case:{All_Case},<span style="color:green;">passed:{passed},<span style="color:red;">failed:{failed}</p>
    <table>
    </table>
    <table border="1"
cellpadding="10">
        <tbody>
        <tr bgcolor="MintCream">
            <th>case_id</th>
            <th>case_result</th>
            <th>case_img</th>
            <th>case_per</th>
            <th>case_log</th>
            <th>case_filter_log</th>
        </tr>
            %(tr)s

        </tbody>
    </table>
    </body>
    </html>
    '''.format(Time=U.get_now_time(), device=device, app_info=app_info, All_Case=all_case, passed=passed, failed=failed)
    data = {'tr': log}
    save_html_file = '%s/test.html' % result_path
    with open(save_html_file, 'w') as f:
        f.write(template % data)
        f.close()
    return save_html_file


if __name__ == '__main__':
    a = get_html_tr(1, '问问问', '/Users/joko/Documents/Auto_Analysis/status/2016-11-08_10_50_34/zefsd.jpg', 'kahsdkhaskd')
    get_html(''.join(a), '123123')
