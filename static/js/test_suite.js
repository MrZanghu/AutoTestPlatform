function selectOrCancelAll() {
    var $all_select = document.getElementById("all_select").checked;
    var $testsuite_list = document.querySelectorAll('tbody input');

    if ($all_select) {
        // 全选
        for (var i = 0; i < $testsuite_list.length; i++) {
            $testsuite_list[i].checked = true;
        }
    } else
        //取消全选
    {
        for (var j = 0; j < $testsuite_list.length; j++) {
            $testsuite_list[j].checked = false;
        }
    }
}

function ischecked() {
    var $allCheck = document.getElementsByName("testsuite_list");
    //遍历每一个复选框，为true则上传
    for (var i = 0; i < $allCheck.length; i++) {
            if ($allCheck[i].checked === true) {
                alert("点击确认，30秒后执行集合，跳转至执行结果页等待");
                return true;
            }
        }
    alert("请选择要执行的测试集合");
    return false;
}