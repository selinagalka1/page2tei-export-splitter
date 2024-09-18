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
    
    <!-- Remove empty attributes -->
    <xsl:template match="@*[.='']">
        <!-- Do nothing to remove the attribute -->
    </xsl:template>
    
    <!-- Transform <tei:digitization_error> to <sic> -->
    <xsl:template match="tei:digitization_error">
        <!-- Explicitly specify the default namespace for <sic> -->
        <xsl:element name="sic" namespace="http://www.tei-c.org/ns/1.0">
            <xsl:attribute name="ana">digitization_error</xsl:attribute>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>
    
    <!-- Ensure <tei:digitization_error> text nodes are copied correctly -->
    <xsl:template match="tei:digitization_error/text()">
        <xsl:copy/>
    </xsl:template>
    
</xsl:stylesheet>
