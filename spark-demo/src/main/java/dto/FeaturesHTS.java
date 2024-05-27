package dto;

/**
 * 日志中提取的时间与空间的特征
 */
public class FeaturesHTS {

    //驻留页面的平均时间
    private String averageDurTime;
    //驻留页面时间的标准差
    private String durStd;
    //session会话的持续时间
    private String durSum;
    //访问的数据量大小
    private String bytesSum;
    //驻留时间的序列
    private String durArray;
    //html率
    private String htmlRate;
    //image率
    private String imageRate;
    //css率
    private String cssRate;
    //js率
    private String jsRate;
    //其他资源率
    private String resourceOtherRate;
    //get方法率
    private String methodGetRate;
    //post方法率
    private String methodPostRate;
    //head方法率
    private String methodHeadRate;
    //其他方法率
    private String methodOtherRate;
    //200占比
    private String reponsesSum2xxRate;
    //300占比
    private String reponsesSum3xxRate;
    //400占比
    private String reponsesSum4xxRate;
    //500占比
    private String reponsesSum5xxRate;
    //周末的占比
    private String weekendDayRate;
    //深夜的占比
    private String deepNightTimeRate;
    //工作时间的占比
    private String worktimeRate;
    //休息时间的占比
    private String resttimeRate;

    public String getAverageDurTime() {
        return averageDurTime;
    }

    public void setAverageDurTime(String averageDurTime) {
        this.averageDurTime = averageDurTime;
    }

    public String getDurStd() {
        return durStd;
    }

    public void setDurStd(String durStd) {
        this.durStd = durStd;
    }

    public String getDurSum() {
        return durSum;
    }

    public void setDurSum(String durSum) {
        this.durSum = durSum;
    }

    public String getBytesSum() {
        return bytesSum;
    }

    public void setBytesSum(String bytesSum) {
        this.bytesSum = bytesSum;
    }

    public String getHtmlRate() {
        return htmlRate;
    }

    public void setHtmlRate(String htmlRate) {
        this.htmlRate = htmlRate;
    }

    public String getImageRate() {
        return imageRate;
    }

    public void setImageRate(String imageRate) {
        this.imageRate = imageRate;
    }

    public String getCssRate() {
        return cssRate;
    }

    public void setCssRate(String cssRate) {
        this.cssRate = cssRate;
    }

    public String getJsRate() {
        return jsRate;
    }

    public void setJsRate(String jsRate) {
        this.jsRate = jsRate;
    }

    public String getResourceOtherRate() {
        return resourceOtherRate;
    }

    public void setResourceOtherRate(String resourceOtherRate) {
        this.resourceOtherRate = resourceOtherRate;
    }

    public String getMethodGetRate() {
        return methodGetRate;
    }

    public void setMethodGetRate(String methodGetRate) {
        this.methodGetRate = methodGetRate;
    }

    public String getMethodPostRate() {
        return methodPostRate;
    }

    public void setMethodPostRate(String methodPostRate) {
        this.methodPostRate = methodPostRate;
    }

    public String getMethodHeadRate() {
        return methodHeadRate;
    }

    public void setMethodHeadRate(String methodHeadRate) {
        this.methodHeadRate = methodHeadRate;
    }

    public String getMethodOtherRate() {
        return methodOtherRate;
    }

    public void setMethodOtherRate(String methodOtherRate) {
        this.methodOtherRate = methodOtherRate;
    }

    public String getReponsesSum2xxRate() {
        return reponsesSum2xxRate;
    }

    public void setReponsesSum2xxRate(String reponsesSum2xxRate) {
        this.reponsesSum2xxRate = reponsesSum2xxRate;
    }

    public String getReponsesSum3xxRate() {
        return reponsesSum3xxRate;
    }

    public void setReponsesSum3xxRate(String reponsesSum3xxRate) {
        this.reponsesSum3xxRate = reponsesSum3xxRate;
    }

    public String getReponsesSum4xxRate() {
        return reponsesSum4xxRate;
    }

    public void setReponsesSum4xxRate(String reponsesSum4xxRate) {
        this.reponsesSum4xxRate = reponsesSum4xxRate;
    }

    public String getReponsesSum5xxRate() {
        return reponsesSum5xxRate;
    }

    public void setReponsesSum5xxRate(String reponsesSum5xxRate) {
        this.reponsesSum5xxRate = reponsesSum5xxRate;
    }

    public String getWeekendDayRate() {
        return weekendDayRate;
    }

    public void setWeekendDayRate(String weekendDayRate) {
        this.weekendDayRate = weekendDayRate;
    }

    public String getDeepNightTimeRate() {
        return deepNightTimeRate;
    }

    public void setDeepNightTimeRate(String deepNightTimeRate) {
        this.deepNightTimeRate = deepNightTimeRate;
    }

    public String getWorktimeRate() {
        return worktimeRate;
    }

    public void setWorktimeRate(String worktimeRate) {
        this.worktimeRate = worktimeRate;
    }

    public String getResttimeRate() {
        return resttimeRate;
    }

    public void setResttimeRate(String resttimeRate) {
        this.resttimeRate = resttimeRate;
    }

    public String getDurArray() {
        return durArray;
    }

    public void setDurArray(String durArray) {
        this.durArray = durArray;
    }

    @Override
    public String toString() {
        return "FeaturesHTS{" +
                "averageDurTime='" + averageDurTime + '\'' +
                ", durStd='" + durStd + '\'' +
                ", durSum='" + durSum + '\'' +
                ", bytesSum='" + bytesSum + '\'' +
                ", durArray='" + durArray + '\'' +
                ", htmlRate='" + htmlRate + '\'' +
                ", imageRate='" + imageRate + '\'' +
                ", cssRate='" + cssRate + '\'' +
                ", jsRate='" + jsRate + '\'' +
                ", resourceOtherRate='" + resourceOtherRate + '\'' +
                ", methodGetRate='" + methodGetRate + '\'' +
                ", methodPostRate='" + methodPostRate + '\'' +
                ", methodHeadRate='" + methodHeadRate + '\'' +
                ", methodOtherRate='" + methodOtherRate + '\'' +
                ", reponsesSum2xxRate='" + reponsesSum2xxRate + '\'' +
                ", reponsesSum3xxRate='" + reponsesSum3xxRate + '\'' +
                ", reponsesSum4xxRate='" + reponsesSum4xxRate + '\'' +
                ", reponsesSum5xxRate='" + reponsesSum5xxRate + '\'' +
                ", weekendDayRate='" + weekendDayRate + '\'' +
                ", deepNightTimeRate='" + deepNightTimeRate + '\'' +
                ", worktimeRate='" + worktimeRate + '\'' +
                ", resttimeRate='" + resttimeRate + '\'' +
                '}';
    }
}
