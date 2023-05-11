function selectOrCancelAll() {
    var $all_select = document.getElementById("all_select").checked;
    var $testcases_list = document.querySelectorAll('tbody input');

    if ($all_select) {
        // 全选
        for (var i = 0; i < $testcases_list.length; i++) {
            $testcases_list[i].checked = true;
        }
    } else
        //取消全选
    {
        for (var j = 0; j < $testcases_list.length; j++) {
            $testcases_list[j].checked = false;
        }
    }
}

function ischecked() {
    var $allCheck = document.getElementsByName("testcases_list");
    //遍历每一个复选框，为true则上传
    for (var i = 0; i < $allCheck.length; i++) {
        if ($allCheck[i].checked === true) {
            alert("点击确认执行用例，跳转至执行结果页等待");


            var $ex_case = document.getElementsByName("ex_case");
            var $ex_time = document.getElementsByName("ex_time").item(0).value;

            if ($ex_case) {
                $.getJSON("/atp/test_case/atp/get_job_name/", {"ex_time":$ex_time},function (data) {
                    console.log("ok");
                });
            }


            return true;
        }
    }
    alert("请选择要执行的测试用例");
    return false;
}

$(function () {
    $("#upload-xls").click(function () {
        alert("点击确认，上传模板文件，请30秒后查看");
    });
})