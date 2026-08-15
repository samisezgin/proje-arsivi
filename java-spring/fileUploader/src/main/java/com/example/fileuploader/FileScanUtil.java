package com.example.fileuploader;

import com.kanishka.virustotal.dto.FileScanReport;
import com.kanishka.virustotal.dto.ScanInfo;
import com.kanishka.virustotal.dto.VirusScanInfo;
import com.kanishka.virustotal.exception.APIKeyNotFoundException;
import com.kanishka.virustotal.exception.QuotaExceededException;
import com.kanishka.virustotal.exception.UnauthorizedAccessException;
import com.kanishka.virustotalv2.VirusTotalConfig;
import com.kanishka.virustotalv2.VirustotalPublicV2;
import com.kanishka.virustotalv2.VirustotalPublicV2Impl;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.Map;

public class FileScanUtil {
    private static final String API_KEY = "2c5421cd66d9559e919848b3278d5cea12e2f16e077d84c201244a219d107f5c";

    /**
     * @param file
     * @return
     */
    public static int scanFile(File file) throws APIKeyNotFoundException, QuotaExceededException, UnauthorizedAccessException, IOException {
        VirusTotalConfig.getConfigInstance().setVirusTotalAPIKey(API_KEY);
        VirustotalPublicV2 virusTotalRef = new VirustotalPublicV2Impl();
        ScanInfo scanInformation = virusTotalRef.scanFile(file);
        return getFileScanReport(scanInformation.getResource());
    }


    public static int getFileScanReport(String resource) {
        try {
            VirusTotalConfig.getConfigInstance().setVirusTotalAPIKey(API_KEY);
            VirustotalPublicV2 virusTotalRef = new VirustotalPublicV2Impl();

            Map<String, VirusScanInfo> scans;
            FileScanReport report = virusTotalRef.getScanReport(resource);
            scans = report.getScans();
            int timeForScan = 0;
            while (scans == null) {
                Thread.sleep(15000);
                timeForScan += 15;
                report = virusTotalRef.getScanReport(resource);
                scans = report.getScans();
                System.out.println("Waiting for scan results for: " + timeForScan + "s");
            }

            for (String key : scans.keySet()) {
                VirusScanInfo virusInfo = scans.get(key);
                var result = virusInfo.getResult();
                if (result != null) {
                    return 400;
                }
            }

        } catch (APIKeyNotFoundException ex) {
            System.err.println("API Key not found! " + ex.getMessage());
            return 401;
        } catch (UnsupportedEncodingException ex) {
            System.err.println("Unsupported Encoding Format!" + ex.getMessage());
            return 402;
        } catch (UnauthorizedAccessException ex) {
            System.err.println("Invalid API Key " + ex.getMessage());
            return 403;
        } catch (Exception ex) {
            System.err.println("Something Bad Happened! " + ex.getMessage());
            return 404;
        }

        return 200;
    }
}
