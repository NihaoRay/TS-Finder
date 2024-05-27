package org.example

import com.alibaba.fastjson.{JSON, JSONObject}
import dto.FeaturesHTS
import org.apache.commons.lang3.StringUtils

import java.util
import java.util.{Calendar, Date}
import scala.util.control.Breaks.{break, breakable}

object SparkUtils {

  /**
   * 匹配分组后的日志
   *
   * @param logList ip为key，对应这流量集合
   */
  def matchLogRule(logList: Iterable[JSONObject]): util.ArrayList[String] = {
    var beforeTimestamp = 0L
    var timeSum = 0L

    //计算驻留时间，并找出分割的位置得出session会话列表
    val sessionIndexList = new util.ArrayList[Int]()
    var index = 0
    logList.foreach(item => {
      val timestamp = item.getLong("time")
      //计算访问时间间隔，第一条设置为0
      var dur = timestamp - beforeTimestamp
      if (index == 0) {
        dur = 0
      }
      item.put("dur", dur)

      // 访问间隔时间30分钟以内
      if (dur > 1800) {
        sessionIndexList.add(index)
      }
      if (timestamp != null) {
        timeSum += timestamp
        beforeTimestamp = timestamp
      }
      index += 1
    })

    //根据IP下的数据流量，根据分割规则提取到的下标，进行分割
    val sliceList = new util.ArrayList[Iterable[JSONObject]]()
    var beforeSliceIndex = 0
    sessionIndexList.forEach(item => {
      sliceList.add(logList.slice(beforeSliceIndex, item))
      beforeSliceIndex = item
    })
    if (beforeSliceIndex <= logList.size) {
      sliceList.add(logList.slice(beforeSliceIndex, logList.size))
    }

    logrule(sliceList)
  }

  /**
   *
   * @param sliceList 根据访问的时间间隔分割的会话的流量数据
   * @return
   */
  private def logrule(sliceList: util.ArrayList[Iterable[JSONObject]]): util.ArrayList[String] = {
    val featuresList = new util.ArrayList[String]
    sliceList.forEach(item => {

//      val featureArray = new util.ArrayList[String]()
      val featuresHTS = new FeaturesHTS

      //时间序列的特征提取：平均访问时间、访问的时间的标准差、计算session持续时间、访问的数据量大小、访问的时间序列
      sessionSizeFeature(item, featuresHTS)
      //识别请求资源情况 请求html总数、css总数、image总数、js总数
      getRequestType(item, featuresHTS)
      getMethodType(item, featuresHTS)
      getResponseCode(item, featuresHTS)
      getWeekend(item, featuresHTS)

      featuresList.add(JSON.toJSONString(featuresHTS))
    })

    featuresList
  }

  /**
   * 提取会话值的特征
   *
   * @param sessionIter session会话中每条的日志记录
   * @return (平均访问时间、访问的时间的标准差、计算session持续时间、访问的数据量大小、访问的时间序列)
   */
  private def sessionSizeFeature(sessionIter: Iterable[JSONObject], featuresHTS: FeaturesHTS): Unit = {
    val sessionList: List[JSONObject] = sessionIter.toList
    val sessionSize = sessionList.size
    //每个session的第一条的访问驻留时间（dur）强制设置为0
    sessionList.head.put("dur", 0)

    //可以用来持续时间，访问平均时间
    var durSum = 0L
    //访问的数据量大小
    var bytesSum = 0L
    val durArray = new util.ArrayList[String]()
    sessionIter.foreach(logflow => {

      val dur = logflow.getLong("dur")
      val bytes = logflow.getLong("bytes")

      durArray.add(String.valueOf(dur))

      durSum += dur
      bytesSum += bytes
    })

    //平均时间
    var averageDurTime = 0d
    if (sessionSize > 0) {
      averageDurTime = durSum.toDouble / sessionSize
    }

    //访问时间的方差
    var variance = 0d
    sessionIter.foreach(logflow => {
      variance += Math.pow(logflow.getLong("dur") - averageDurTime, 2)
    })
    var durStd = 0d
    if (sessionSize > 1) {
      durStd = Math.sqrt(variance / sessionSize)
    }

    featuresHTS.setAverageDurTime(String.valueOf(averageDurTime))
    featuresHTS.setDurStd(String.valueOf(durStd))
    featuresHTS.setDurSum(String.valueOf(durSum))
    featuresHTS.setBytesSum(String.valueOf(bytesSum))
    featuresHTS.setDurArray(durArray.toArray.mkString(","))
  }

  /**
   * 提取会话中日志的请求类型
   *
   * @param sessionIter session会话中每条的日志记录
   * @return 返回html, css, image, js以及其他资源的请求数据量占比
   */
  private def getRequestType(sessionIter: Iterable[JSONObject], featuresHTS: FeaturesHTS) = {
    var htmlSum = 0
    var cssSum = 0
    var imageSum = 0
    var jsSum = 0
    var otherSum = 0

    sessionIter.foreach(item => {
      //提取请求的连接
      val request = item.getString("referrer")
      breakable {
        //统计html
        if (StringUtils.isBlank(request)) {
          htmlSum += 1
          break()
        }
        val requestParam = request.split("\\?")
        if (!request.contains(".") || "/".equals(request)) {
          htmlSum += 1
          break()
        }

        //统计image
        if (requestParam.size > 1 && (requestParam.take(1).endsWith(".jpg")
          || requestParam.take(1).endsWith(".jpg")
          || requestParam.take(1).endsWith(".gif")
          || requestParam.take(1).endsWith(".jpeg"))) {
          imageSum += 1
          break()
        }
        val htmlShow = request.startsWith("/Cover/Show")
        if (htmlShow || request.contains(".jpg")
          || request.contains(".png") || request.contains("/images/")) {
          imageSum += 1
          break()
        }

        //统计ss
        if (requestParam.size > 1 && (requestParam.take(1).endsWith(".css")
          || requestParam.take(0).endsWith(".css"))) {
          cssSum += 1
          break()
        }
        if (request.contains("/css")) {
          cssSum += 1
          break()
        }

        //统计js
        if (requestParam.size > 1 && requestParam.take(1).endsWith(".js")
          || requestParam.take(0).endsWith(".js")) {
          jsSum += 1
          break()
        }
        if (request.endsWith(".js")) {
          jsSum += 1
        }
      }
    })

    //统计其他的页面总量
    val sessionSize = sessionIter.size
    otherSum = sessionSize - (htmlSum + imageSum + cssSum + jsSum)

    featuresHTS.setHtmlRate(String.valueOf(htmlSum.toDouble / sessionSize))
    featuresHTS.setImageRate(String.valueOf(imageSum.toDouble / sessionSize))
    featuresHTS.setCssRate(String.valueOf(cssSum.toDouble / sessionSize))
    featuresHTS.setJsRate(String.valueOf(jsSum.toDouble / sessionSize))
    featuresHTS.setResourceOtherRate(String.valueOf(otherSum.toDouble / sessionSize))
  }

  /**
   * 获取http method的数量占比
   *
   * @param sessionIter session会话中每条的日志记录
   * @return 返回get、post、head以及其他请求方法数量的占比
   */
  private def getMethodType(sessionIter: Iterable[JSONObject], featuresHTS: FeaturesHTS) = {
    var getSum = 0
    var postSum = 0
    var headSum = 0

    sessionIter.foreach(item => {
      val method = item.getString("method")
      breakable {
        if (StringUtils.isBlank(method)) {
          break()
        }

        if ("get".equals(method.toLowerCase())) {
          getSum += 1
          break()
        }

        if ("post".equals(method.toLowerCase())) {
          postSum += 1
          break()
        }

        if ("head".equals(method.toLowerCase())) {
          headSum += 1
          break()
        }
      }
    })

    val sessionSize = sessionIter.size
    val otherSum = sessionSize - (getSum + postSum + headSum)

    featuresHTS.setMethodGetRate(String.valueOf(getSum.toDouble / sessionSize))
    featuresHTS.setMethodPostRate(String.valueOf(postSum.toDouble / sessionSize))
    featuresHTS.setMethodHeadRate(String.valueOf(headSum.toDouble / sessionSize))
    featuresHTS.setMethodOtherRate(String.valueOf(otherSum.toDouble / sessionSize))
  }

  /**
   * 获的response code的数量占比
   *
   * @param sessionIter session会话中每条的日志记录
   * @return 返回get、post、head以及其他请求方法数量的占比
   */
  private def getResponseCode(sessionIter: Iterable[JSONObject], featuresHTS: FeaturesHTS) = {
    var sum2xx = 0
    var sum3xx = 0
    var sum4xx = 0
    var sum5xx = 0

    sessionIter.foreach(item => {
      val responseCode = item.getIntValue("response")
      breakable {
        if ((200 <= responseCode) && (responseCode < 300)) {
          sum2xx += 1
          break()
        }
        if ((300 <= responseCode) && (responseCode < 400)) {
          sum3xx += 1
          break()
        }
        if ((400 <= responseCode) && (responseCode < 500)) {
          sum4xx += 1
          break()
        }
        sum5xx += 1
      }
    })

    val sessionSize = sessionIter.size

    featuresHTS.setReponsesSum2xxRate(String.valueOf(sum2xx.toDouble / sessionSize))
    featuresHTS.setReponsesSum3xxRate(String.valueOf(sum3xx.toDouble / sessionSize))
    featuresHTS.setReponsesSum4xxRate(String.valueOf(sum4xx.toDouble / sessionSize))
    featuresHTS.setReponsesSum5xxRate(String.valueOf(sum5xx.toDouble / sessionSize))
  }

  /**
   * 计算weekend day，深夜访问、7到12点之间的访问时间、工作访问时间 占比
   * @param sessionIter session会话中每条的日志记录
   * @return
   */
  private def getWeekend(sessionIter: Iterable[JSONObject], featuresHTS: FeaturesHTS) = {
    var weekendDaySum = 0
    var deepNightTimeSum = 0
    var worktimeSum = 0
    var resttimeSum = 0
    val calendar = Calendar.getInstance

    sessionIter.foreach(item => {
      val time = item.getIntValue("time")
      calendar.setTime(new Date(time))
      val weekday = calendar.get(Calendar.DAY_OF_WEEK)
      val hours = calendar.get(Calendar.HOUR_OF_DAY)

      breakable {
        if ((5 <= weekday) && (weekday < 6)) {
          weekendDaySum += 1
          break()
        }
        if ((0 <= hours) && (hours < 7)) {
          deepNightTimeSum += 1
          break()
        }
        if (19 <= hours) {
          resttimeSum += 1
          break()
        }
        if ((7 < hours) && (hours < 19))
          worktimeSum += 1
      }
    })

    val sessionSize = sessionIter.size.toDouble

    featuresHTS.setWeekendDayRate(String.valueOf(weekendDaySum / sessionSize))
    featuresHTS.setDeepNightTimeRate(String.valueOf(deepNightTimeSum / sessionSize))
    featuresHTS.setWorktimeRate(String.valueOf(worktimeSum / sessionSize))
    featuresHTS.setResttimeRate(String.valueOf(resttimeSum / sessionSize))
  }

  


  //  val timestamp = item.getLong("time")
  //  val referrer = item.getString("referrer")
  //  val method = item.getString("method")
  //  val request = item.getString("request")
  //  val response = item.getString("response")
  //  val bytes = item.getLong("bytes")
  //  val useragent = item.getString("useragent")
  //  val resource = item.getString("resource")
  //  val ip = item.getString("ip")


}
