import os,re
import json,zipfile
import traceback
import requests,logging
from json import JSONDecodeError
from main_platform import viewsParams as vp



logger= logging.getLogger("main_platform")


def preprocess_request_data(request_data,global_key,related_case_id,output):
    '''
    对于有调用全局变量的用例，进行数据预处理
    :param request_data:
    :return: 返回需要调用的参数
    '''
    try:
        related_cid= "current_id_%s" % str(related_case_id)
        global_var= json.loads(os.environ[global_key])[related_cid]
        requestData= request_data
        for var_name in re.findall(r"\$\{(\w+)\}", request_data):
            requestData= re.sub(r"\$\{%s\}" % var_name, str(global_var[var_name]), requestData)
            # 进行请求参数替换
        if output== 0:
            return (vp.Y_INPUT_NO_OUTPUT, requestData, "ok") # 有入参，无出参
        else:
            return (vp.Y_INPUT_Y_OUTPUT, requestData, "ok") # 有入参，有出参
        # raise ZeroDivisionError # 测试其他Exception使用
    except Exception as e:
        logger.info("请求数据预处理发生异常，error：{}".format(traceback.format_exc(limit= 3)))
        return 0, request_data, traceback.format_exc()


def request_process(url, request_method, request_data):
    '''
    封装get、post、put请求方法，返回响应数据
    :param url: 测试地址
    :param request_method:请求方法
    :param request_data:请求数据
    :return:
    '''
    logger.info("-------- 开始调用接口 --------")
    if request_method== "get":
        try:
            rd= json.loads(request_data)    # json.loads将str转为dict，如果可以转换则使用params
            result= requests.get(url, params= rd)
            logger.info("接口地址:%s" % result.url)
            logger.info("请求数据:%s" % request_data)
            # raise ZeroDivisionError # 测试其他Exception使用
        except JSONDecodeError:
            rd= request_data
            result= requests.get(url + str(rd))
            logger.info("接口地址:%s" % result.url)
            logger.info("请求数据:%s" % request_data)
        except Exception as e:
            # 除了JSONDecodeError之外的报错
            logger.info("get方法请求发生异常:请求的url是:%s，请求的内容是:%s，"
                        "发生的异常信息如下:%s" % (url, request_data, e))
            result= "get方法请求发生异常:请求的url是:%s,请求的内容是:%s," \
                    "发生的异常信息如下:%s" % (url, request_data, e)
        return result

    elif request_method== "post":
        try:
            rd= json.loads(request_data)    # json.loads将str转为dict
            result= requests.post(url, data= rd)
            logger.info("接口地址:%s" % result.url)
            logger.info("请求数据:%s" % request_data)
            # raise ZeroDivisionError # 测试其他Exception使用
        except JSONDecodeError:
            logger.info("post方法请求发生异常:请求的url是:%s，请求的内容是:%s,"
                        "发生的异常信息如下:%s" % (url, request_data, "请求参数不是dict"))
            result= "post方法请求发生异常:请求的url是:%s,请求的内容是:%s," \
                    "发生的异常信息如下:%s" % (url, request_data, "请求参数不是dict")
        except Exception as e:
            # 除了JSONDecodeError之外的报错
            logger.info("post方法请求发生异常:请求的url是:%s，请求的内容是:%s，"
                        "发生的异常信息如下:%s" % (url, request_data, e))
            result= "post方法请求发生异常:请求的url是:%s,请求的内容是:%s," \
                    "发生的异常信息如下:%s" % (url, request_data, e)
        return result

    elif request_method== "put":
        try:
            rd= json.loads(request_data)    # json.loads将str转为dict
            result= requests.put(url, data= rd)
            logger.info("接口地址:%s" % result.url)
            logger.info("请求数据:%s" % request_data)
            # raise ZeroDivisionError # 测试其他Exception使用
        except JSONDecodeError:
            logger.info("put方法请求发生异常:请求的url是:%s，请求的内容是:%s，"
                        "发生的异常信息如下:%s" % (url, request_data, "请求参数不是dict"))
            result= "put方法请求发生异常:请求的url是:%s,请求的内容是:%s," \
                    "发生的异常信息如下:%s" % (url, request_data, "请求参数不是dict")
        except Exception as e:
            # 除了JSONDecodeError之外的报错
            logger.info("put方法请求发生异常:请求的url是:%s，请求的内容是:%s，"
                        "发生的异常信息如下:%s" % (url, request_data, e))
            result= "put方法请求发生异常:请求的url是:%s,请求的内容是:%s," \
                    "发生的异常信息如下:%s" % (url, request_data, e)
        return result


def get_var_from_response(global_key, response_data, extract_var,current_id):
    '''
    从相应数据中，根据变量提取公式，提取全局变量，用于其他接口用例使用
    :param global_key:
    :param response_data:接口返回值
    :param extract_var:全局变量公式
    :return:
    '''
    logger.info("变量公式:%s" % extract_var)
    try:
        extract_var_list= extract_var.split(";") # 处理多个提取参数
        new_dict= json.loads(os.environ[global_key])

        for evl in extract_var_list:
            var_name= evl.split("||")[0]
            logger.info("变量名称:%s" % var_name)
            regx_exp= evl.split("||")[1]
            logger.info("提取正则:%s" % regx_exp)

            if re.search(regx_exp, response_data):
                global_vars= json.loads(os.environ[global_key])[current_id] # 获取全局变量中的当前case信息
                var_value= re.search(regx_exp, response_data).group(1) # 返回括号匹配第一个成功的
                global_vars[var_name]= var_value
                new_dict[current_id]= global_vars
                os.environ[global_key]= json.dumps(new_dict)
                # {"current_id_14": {"code": "200", "ip": "192.168.31.134"}, "current_id_15": {"method": "get"}}
            else:
                raise Exception
        logger.info("现全局变量:{}".format(os.environ[global_key]))
        return new_dict[current_id]
    except Exception as e:
        logger.info("无法提取参数，请求公式为{}".format(extract_var))
        return None


def zip_file(src_dir:str,name:str,file_list:list):
    '''
    处理集合报告文件压缩
    :param src_dir: 路径地址
    :param name: zip报告文件名称
    :param file_list: 报告具体名称
    :return:
    '''
    src_dir_all= os.getcwd()+src_dir
    zip_name= src_dir_all+name+".zip"

    z= zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(src_dir_all):
        fpath= root.replace(src_dir_all, '')
        fpath= fpath and fpath + os.sep or '' # 为了去除压缩后有绝对路径
        for filename in files:
            if filename[-24:-5] in file_list:
                z.write(os.path.join(root, filename),fpath+filename)
                os.remove(os.path.join(root, filename))
            else:
                pass
    z.close()