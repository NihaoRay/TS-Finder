package org.example

import com.alibaba.fastjson.JSON
import manager.AppConfigManager
import org.apache.commons.lang3.StringUtils
import org.apache.spark.sql.SparkSession

import java.text.SimpleDateFormat

/**
 * @author ${user.name}
 */
object Dataflow {

  def main(args: Array[String]): Unit = {

    //获取运行环境并加载对应的配置文件
    if (args == null || args.length < 1) {
      println(
        s"""
           |Usage：<runMode>
           |runMode：flag of different environment
                """.stripMargin)
      System.exit(-1)
    }
    val runMode = args(0).trim
    val props = AppConfigManager.getProperties(runMode)

    //用于测试能否调用Java类对象和方法
    //    val deta = new Dataset
    //    print(deta.demo())
    //时间的日期格式，用于转换时间戳
    val formatMs = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'.'SSSX")
    //匹配数据集中的id中的内容
    val regex = """^"(-|_)?[-a-zA-Z0-9_]+((-|_)+|(-|_)?)":""".r
    val spark = SparkSession
      .builder()
      .master(props.getProperty("spark.master"))
      .appName(props.getProperty("appName"))
      //      .config("spark.some.config.option", "some-value")
      .getOrCreate()


    val textFile = spark.sparkContext
      //      .textFile("hdfs://192.168.31.152:8020/ml_dataflow/public_v2.json")
      //      .textFile("hdfs://node1:9000/new.txt")
      .textFile(props.getProperty("hdfs.filepath"))

    //首先过滤器选择具有referrer字段的数据内容，没有的则过滤掉
    val referrerRDD = textFile.filter(line => {
      line.contains("referrer")
    }).map(item => {
      //格式化数据，转为JSONObject的格式
      val replaceStr = regex.findFirstIn(item).get
      val requestJSON = JSON.parseObject(item.replace(replaceStr, ""))
      //将日期转为时间戳，作为排序的键
      val timestamp = formatMs.parse(requestJSON.getString("timestamp")).getTime
      requestJSON.put("time", timestamp/1000)
      //以ip为spark中的pair key
      (requestJSON.getString("ip"), requestJSON)
    }).filter(x => StringUtils.isNotBlank(x._1)).sortBy(x => x._2.getLong("time"))

    //对数据进行分组组成在一起，形成一个key对应多条数据的关系
    val aggRDD = referrerRDD.groupByKey().map(x => {
      val logList = x._2

      val featuresStr = SparkUtils.matchLogRule(logList)
      featuresStr.toArray
    })

    //    baseRDD.top(10).foreach(item => println(item))
    aggRDD.flatMap(item => item).take(20).foreach(item => {
      println(item)
    })
    //将结果输出到文件中
//    aggRDD.flatMap(item => item).saveAsTextFile(props.getProperty("hdfs.dataflow.path"))



    //    D:\workspace\spark-3.3.2-bin-hadoop3-scala2.13\examples\src\main\resources

    //    D:\workspace\spark-3.3.2-bin-hadoop3-scala2.13\examples\src\main\resources


    // Displays the content of the DataFrame to stdout


    //
    //    //设置Spark任务的配置选项
    //    //setAppName("ScalaWordCount")：设置APP的名字为：ScalaWordCount
    //    //setMaster("local")：设置Spark任务的运行模式为本地模式，不设的话，默认是Spark集群模式
    //    val conf = new SparkConf().setAppName("ScalaWordCount").setMaster("local")
    //
    //    //根据配置创建SparkContext对象
    //    val sc = new SparkContext(conf)
    //
    //    //从本地磁盘读入数据
    //    val lines = sc.textFile("D:\\workspace\\ml_dataset\\ids-dataset\\UNSW-NB15-CSVFiles\\merge_out.csv")
    //
    //    //进行分词操作
    //    val words = lines.flatMap(_.split(" "))
    //
    //    //Map操作：每个单词记一次数
    //    val wordPair = words.map((_, 1)) //完整写法： words.map(x => (x,1))
    //
    //    //Reduce操作：将相同的Key的Value相加
    //    val wordcount = wordPair.reduceByKey(_ + _)
    //
    //    //调用Action算子：collect触发计算
    //    val result = wordcount.collect()
    //
    //    //将结果打印在屏幕上
    //    result.foreach(println)
    //
    //    //停止SparkContext对象
    //    sc.stop()
  }

}
