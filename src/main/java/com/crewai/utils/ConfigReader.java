package com.crewai.utils;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import java.io.FileReader;

public class ConfigReader {
    private static JSONObject config;

    static {
        try {
            JSONParser parser = new JSONParser();
            config = (JSONObject) parser.parse(new FileReader("src/test/resources/config.json"));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String getBaseUrl() {
        return (String) config.get("baseUrl");
    }

    public static long getTimeout() {
        return (Long) config.get("timeout");
    }

    public static String getBrowser() {
        return (String) config.get("browser");
    }

    public static JSONObject getEnvironmentConfig(String env) {
        JSONObject environments = (JSONObject) config.get("environments");
        return (JSONObject) environments.get(env);
    }
}