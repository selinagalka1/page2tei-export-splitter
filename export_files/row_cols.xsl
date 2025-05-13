<xsl:stylesheet version="2.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">
    
    <xsl:variable name="source" select="document('file_1763_wien.xml')" />
    <xsl:preserve-space elements="*"/>
    
    <!-- Identity transform -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>
    
    <!-- Match <row> -->
    <xsl:template match="tei:row">
        <xsl:variable name="match" select="$source//tei:row[@facs = current()/@facs][1]" />
        <xsl:copy>
            <!-- Copy all attributes except rows/cols -->
            <xsl:apply-templates select="@*[name() != 'rows' and name() != 'cols']" />
            <!-- Add correct rows/cols from source if present -->
            <xsl:if test="$match/@rows">
                <xsl:attribute name="rows"><xsl:value-of select="$match/@rows" /></xsl:attribute>
            </xsl:if>
            <xsl:if test="$match/@cols">
                <xsl:attribute name="cols"><xsl:value-of select="$match/@cols" /></xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template>
    
    <!-- Match <cell> -->
    <xsl:template match="tei:cell">
        <xsl:variable name="match" select="$source//tei:cell[@facs = current()/@facs][1]" />
        <xsl:copy>
            <xsl:apply-templates select="@*[name() != 'rows' and name() != 'cols']" />
            <xsl:if test="$match/@rows">
                <xsl:attribute name="rows"><xsl:value-of select="$match/@rows" /></xsl:attribute>
            </xsl:if>
            <xsl:if test="$match/@cols">
                <xsl:attribute name="cols"><xsl:value-of select="$match/@cols" /></xsl:attribute>
            </xsl:if>
            <xsl:apply-templates select="node()" />
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="tei:lb">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="@anchored"></xsl:template>
    
</xsl:stylesheet>
