<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="UTF-8" indent="yes" method="xml" />
 
 
    <xsl:template match="/">
      <xsl:apply-templates/>
    </xsl:template>
 
    <xsl:template match="suite">
        <xsl:param name="count" select="1"/>

        <xsl:variable name="tests" select="count(descendant::compiledtest)" />
 
        <xsl:variable name="errorCount" select="count(descendant::compiledtest/verdict[text()='Error'])" />
        <xsl:variable name="failureCount" select="count(descendant::compiledtest/verdict[text()='Failed'])" />
        <xsl:variable name="totalDuration" select="sum(descendant::compiledtest/duration)" />

        <xsl:choose>
         <xsl:when test="$count > 0">
          <testsuite>
            <xsl:attribute name="name">
                <xsl:value-of select="classname" />
            </xsl:attribute>
            <xsl:attribute name="tests">
                <xsl:value-of select="$tests" />
            </xsl:attribute>
            <xsl:attribute name="errors">
                <xsl:value-of select="$errorCount" />
            </xsl:attribute>
            <xsl:attribute name="failures">
                <xsl:value-of select="$failureCount" />
            </xsl:attribute>
            <xsl:attribute name="name">
                <xsl:value-of select="classname" />
            </xsl:attribute>
            <xsl:attribute name="time">
                <xsl:value-of select="$totalDuration" />
            </xsl:attribute>
            <xsl:apply-templates select="compiledtest" />
            <xsl:apply-templates select="suite">
                 <xsl:with-param name="count" select="$count - 1"/>
            </xsl:apply-templates>     
            <system-out><![CDATA[]]></system-out>
            <system-err><![CDATA[]]></system-err>
          </testsuite>
         </xsl:when>
         <xsl:otherwise>
            <xsl:apply-templates select="compiledtest" />
            <xsl:apply-templates select="suite">
                 <xsl:with-param name="count" select="$count - 1"/>
            </xsl:apply-templates>                
         </xsl:otherwise>
       </xsl:choose>
    </xsl:template>
 

   <xsl:template match="compiledtest">
        <testcase>
            <xsl:attribute name="classname">
                <xsl:value-of select="classname" />
            </xsl:attribute>
            <xsl:attribute name="name">
                <xsl:value-of select="method" />
            </xsl:attribute>
            <xsl:attribute name="time">
                <xsl:value-of select="duration" />
            </xsl:attribute>
            <xsl:if test="verdict[text()='Failed']">
                <failure type="">
                    <xsl:value-of select="failreason" />
                </failure>
            </xsl:if>
            <xsl:if test="verdict[text()='Error']">
                <failure type="">
                    <xsl:value-of select="failreason" />
                </failure>
            </xsl:if>
        </testcase>
    </xsl:template>
</xsl:stylesheet>
