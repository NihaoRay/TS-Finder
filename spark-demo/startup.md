
#### 启动命令

./spark-submit --class org.example.Dataflow \
--master spark://node1:7077 \
--deploy-mode cluster \
hdfs://node1:9000/spark-demo-1.0-SNAPSHOT-jar-with-dependencies.jar dev

命令中的dev是程序接受的外界输入参数，我这里是dev，根据dev选择不同的配置文件，在不同的环境下执行
