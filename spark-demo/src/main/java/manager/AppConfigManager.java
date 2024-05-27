package manager;

import common.SparkConstants;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.StringUtils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/**
 * 应用配置文件管理类
 * Created by chenrui on 2021/4/13
 */
public class AppConfigManager {

    /** 系统配置 */
    private static volatile Properties sysConfig;

    /**
     * 获取系统属性配置
     * @param runMode 运行模式：local-本地；dev-开发环境；test-综测环境；production-生产环境
     * @return 系统配置
     */
    public static Properties getProperties(String runMode) {
        if (sysConfig != null) {
            return sysConfig;
        }
        synchronized (AppConfigManager.class) {
            if (sysConfig != null) {
                return sysConfig;
            }
            if (StringUtils.equals(runMode, SparkConstants.SPARK_RUN_LOCAL)) {
                sysConfig = loadProperties("config/local/application.properties");
            } else if (StringUtils.equals(runMode, SparkConstants.SPARK_RUN_DEV)) {
                sysConfig = loadProperties("config/dev/application.properties");
            } else if (StringUtils.equals(runMode, SparkConstants.SPARK_RUN_TEST)) {
                sysConfig = loadProperties("config/test/application.properties");
            } else if (StringUtils.equals(runMode, SparkConstants.SPARK_RUN_PROD)) {
                sysConfig = loadProperties("config/production/application.properties");
            } else {
                sysConfig = loadProperties("config/local/application.properties");
            }
            return sysConfig;
        }
    }

    /**
     * 加载配置文件
     * @param path 配置文件路径
     * @return 配置文件加载结果
     */
    private static Properties loadProperties(String path) {
        Properties properties = new Properties();
        InputStream is = AppConfigManager.class.getClassLoader().getResourceAsStream(path);
        try {
            properties.load(is);
            System.out.println("load prop success, path: " + path);
        } catch (IOException e) {
            System.out.println("load prop error, path:" + path + ", cause: " + e.getMessage());
            System.exit(1);
        } finally {
            IOUtils.closeQuietly(is);
        }
        return properties;
    }

}
