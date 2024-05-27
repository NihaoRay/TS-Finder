package common;

import java.util.regex.Pattern;

/**
 * 常量类
 * Created by chenrui on 2023/4/13
 */
public class SparkConstants {

    /** sparkStreaming 应用部署模式 */
    public static final String  SPARK_RUN_LOCAL        = "local";                            //本地运行
    public static final String  SPARK_RUN_DEV          = "dev";                              //46环境
    public static final String  SPARK_RUN_TEST         = "test";                             //综测环境
    public static final String  SPARK_RUN_PROD         = "production";                       //生产环境

    /** 配置表存储字段 */
    public static final String  F_MONITOR_ID           = "ID";                               //日志监视器ID
    public static final String  F_LOG_PATH             = "LOG_PATH";                         //日志路径
    public static final String  F_LOG_CONTENT_TYPE     = "LOG_CONTENT_TYPE";                 //日志内容类型
    public static final String  F_INTERFACE_CLASS      = "INTERFACE_CLASS";                  //接口类名
    public static final String  F_INTERFACE_METHOD     = "INTERFACE_METHOD";                 //接口方法名
    public static final String  F_KEYWORDS             = "KEYWORDS";                         //关键字列表
    public static final String  F_EXPRESSION           = "EXPRESSION";                       //关键字表达式
    public static final String  F_KEYWORD_TYPE         = "KEYWORD_TYPE";                     //关键字类型

    /** 日志规则类型 */
    public static final String  RULE_IFS_TYPE          = "IFS";                              //日志接口类型
    public static final String  RULE_ERR_TYPE          = "ERR";                              //异常关键字类型

    /** 关键字类型 */
    public static final String  KEYWORDS_TYPE_REQUEST  = "INVOKE";                           //请求关键字类型
    public static final String  KEYWORDS_TYPE_RESPONSE = "RESPONSE";                         //响应关键字类型
    public static final String  KEYWORDS_TYPE_SUCCESS  = "SUCCESS";                          //成功关键字类型
    public static final String  KEYWORDS_TYPE_FAIL     = "FAIL";                             //失败关键字类型
    public static final String  KEYWORDS_TYPE_DIMEN    = "DIMENSION";                        //多维度关键字类型
    public static final String  KEYWORDS_TYPE_ERR      = "ERROR";                            //异常关键字类型

    /** 存Es库类型标志 */
    public static final String  ES_FLAG_IFS_DIMEN      = "DIMENSION";                        //es存储接口有多维度标志
    public static final String  ES_FLAG_IFS_NO_DIMEN   = "NO_DIMENSION";                     //es存储接口无多维度标志
    public static final String  ES_FLAG_ERR            = "ABNORMAL";                         //es存储异常关键字标志

    /** 耗时正则表达式常量 */
    public static final Pattern CONSUM_TIME_REGEX      = Pattern.compile("(\\[)(\\d*)(ms])");

    /** 写es数据的批量大小 */
    public static final int     BULK_NUM_ES            = 1000;

}
