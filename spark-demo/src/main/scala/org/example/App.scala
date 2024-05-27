package org.example

import com.alibaba.fastjson.JSON
import demo.Dataset
import org.apache.commons.lang3.StringUtils
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.api.java.JavaRDD.fromRDD
import org.apache.spark.sql.SparkSession

import java.text.SimpleDateFormat
import java.util.Date
import java.util.regex.Pattern
import scala.util.control.Breaks.{break, breakable}
import scala.util.parsing.json.JSONObject

/**
 * @author ${user.name}
 */
object App {

  def main(args: Array[String]): Unit = {

    //指定local模式
    val conf = new SparkConf()
//      .setMaster("local[2]")
      .setAppName("read kp data to kafka")

    val sc = new SparkContext(conf)
    //支持通配符路径，支持压缩文件读取
    val rrd = sc.textFile("hdfs://node11:9000/new.txt")
    //提到到集群模式时，去掉uri地址，如果有双namenode，可以自动容灾
    //统计数量
    println(rrd.count())
    //停止spark
    sc.stop()




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
