<?xml version="1.0" encoding="UTF-8"?> 
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei"
    xmlns="http://www.tei-c.org/ns/1.0">
    
    <!-- Identity transformation template -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Remove empty <tei:supplied/> elements -->
    <xsl:template match="tei:supplied[not(node())]">
        <!-- Do nothing: This removes the empty <supplied> element -->
    </xsl:template>
    
    <!-- Add reason attribute to <tei:supplied> -->
    <xsl:template match="tei:supplied">
        <xsl:copy>
            <!-- Add the reason attribute dynamically -->
            <xsl:attribute name="reason">
                <xsl:choose>
                    <!-- Even page -->
                    <xsl:when test="preceding::tei:pb[1]/@facs and number(substring-after(preceding::tei:pb[1]/@facs, '#facs_')) mod 2 = 0">
                        <xsl:value-of select="'binding'"/>
                    </xsl:when>
                    <!-- Odd page -->
                    <xsl:when test="preceding::tei:pb[1]/@facs and number(substring-after(preceding::tei:pb[1]/@facs, '#facs_')) mod 2 = 1">
                        <xsl:value-of select="'cut'"/>
                    </xsl:when>
                    <!-- Default case -->
                    <xsl:otherwise>
                        <xsl:value-of select="'unknown-ab'"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <!-- Apply templates to retain existing content -->
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
