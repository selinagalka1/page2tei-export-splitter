<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei"
    xmlns="http://www.tei-c.org/ns/1.0">
    
    <!-- Identity transformation template (copy everything by default) -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Remove empty <tei:supplied/> elements -->
    <xsl:template match="tei:supplied[not(node())]">
        <!-- Do nothing: This removes the empty <supplied> element -->
    </xsl:template>
    
    <!-- Match non-empty <tei:supplied> elements and add the "reason" attribute -->
    <xsl:template match="tei:table//tei:cell//tei:supplied">
        <xsl:if test="node()"> <!-- Ensure the element is not empty -->
            <xsl:copy>
                <!-- Add the reason attribute dynamically -->
                <xsl:attribute name="reason">
                    <xsl:choose>
                        <!-- Even page and column 1 -->
                        <xsl:when test="number(substring-before(substring-after(ancestor::tei:table/@facs, '#facs_'), '_t')) mod 2 = 0 and ancestor::tei:cell[@n='0']">
                            <xsl:value-of select="'cut'"/>
                        </xsl:when>
                        <!-- Even page and column 3 -->
                        <xsl:when test="number(substring-before(substring-after(ancestor::tei:table/@facs, '#facs_'), '_t')) mod 2 = 0 and ancestor::tei:cell[@n='2']">
                            <xsl:value-of select="'binding'"/>
                        </xsl:when>
                        <!-- Odd page and column 1 -->
                        <xsl:when test="number(substring-before(substring-after(ancestor::tei:table/@facs, '#facs_'), '_t')) mod 2 = 1 and ancestor::tei:cell[@n='0']">
                            <xsl:value-of select="'binding'"/>
                        </xsl:when>
                        <!-- Odd page and column 3 -->
                        <xsl:when test="number(substring-before(substring-after(ancestor::tei:table/@facs, '#facs_'), '_t')) mod 2 = 1 and ancestor::tei:cell[@n='2']">
                            <xsl:value-of select="'cut'"/>
                        </xsl:when>
                    </xsl:choose>
                </xsl:attribute>
                <!-- Apply templates to retain existing content -->
                <xsl:apply-templates select="@*|node()"/>
            </xsl:copy>
        </xsl:if>
    </xsl:template>
    
</xsl:stylesheet>
