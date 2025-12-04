{{/*
Expand the name of the chart.
*/}}
{{- define "oneagent-monitor-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "oneagent-monitor.fullname" -}}
{{- include "oneagent-monitor-chart.fullname" . -}}
{{- end }}

{{- define "oneagent-monitor.labels" -}}
{{- include "oneagent-monitor-chart.labels" . -}}
{{- end }}

{{- define "oneagent-monitor.selectorLabels" -}}
{{- include "oneagent-monitor-chart.selectorLabels" . -}}
{{- end }}

{{- define "oneagent-monitor-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "oneagent-monitor-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "oneagent-monitor-chart.labels" -}}
helm.sh/chart: {{ include "oneagent-monitor-chart.chart" . }}
{{ include "oneagent-monitor-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "oneagent-monitor-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "oneagent-monitor-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}