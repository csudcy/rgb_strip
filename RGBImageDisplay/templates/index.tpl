{% extends 'base.tpl' %}

{% block title %}RGB Image Display Server{% endblock %}

{% block content %}
  <span style="float: left;">
    <ul>
      <li><code>width</code>: {{ width }}</li>
      <li><code>height</code>: {{ height }}</li>
      <li><code>rotate</code>: {{ rotate }}</li>
      <li><code>alpha</code>: {{ alpha }}</li>
      <li><code>delay_seconds</code>: {{ delay_seconds }}</li>
      <li>
        <code>image_groups</code>:
        <ul>
          {% for group_name, images in image_groups.items() %}
            <li>
              <code>{{ group_name }}</code> ({{ images | length }}):
              <ul>
                {% for image_name, image in images %}
                  <li><code>{{ image_name }}</code></li>
                {% endfor %}
              </ul>
            </li>
          {% endfor %}
        </ul>
      </li>
    </ul>
  </span>
  <span>
    <img src="/stream" style="width: {{ width * 7 }}px; height: {{ height * 7 }}px;" />
  </span>
{% endblock %}
