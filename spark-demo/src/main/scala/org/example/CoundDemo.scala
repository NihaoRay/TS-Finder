package org.example

import demo.Dataset
import org.apache.spark.sql.SparkSession

class CoundDemo {

  def main(args: Array[String]) {

    val deta = new Dataset
    print(deta.demo())

    val spark = SparkSession
      .builder()
      .master("local")
      .appName("word demo test")
      .config("spark.some.config.option", "some-value")
      .getOrCreate()

    //    D:\workspace\spark-3.3.2-bin-hadoop3-scala2.13\examples\src\main\resources
    val df = spark.read.json("D:\\workspace\\ml_dataset\\ml_dataflow\\public_v2.json")

    // Displays the content of the DataFrame to stdout
    df.show()



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
