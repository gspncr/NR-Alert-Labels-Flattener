# NR Alert Labels Flattener

![](https://p74.f4.n0.cdn.getcloudapp.com/items/4guyO1pJ/Screenshot%202020-04-28%20at%2013.19.41.png?v=0df28fda97991117bd6bc2910313af85)
Turn this notification channel into this Event:
![](https://p74.f4.n0.cdn.getcloudapp.com/items/WnuGlB8m/Image%202020-04-28%20at%201.15.41%20pm.png?v=c3b34192553d6810b6622f67b8fafd12)

Host the webhook somewhere it is always listening and accessible from New Relic Alerts. 

To start using this, modify the EventAPI variable to match your chosen endpoint. (Find this in Insights -> Manage Data -> API Keys). This is also the location you can generate a new Insert key, or use an existing key - set that in the InsertKey variable.

To extend the properties captured, do this in the payload JSON that is in the **try** statement. You can see in the webhook() function how this is captured - with some additional properties for you to add already. As the script is, it will create a new event called Alerts with attributes *label state*, *account ID, labels flattened.*

If labels are not present a new Event will be added to *NrIntegrationError* with details, as well as to the webhook.log

**Please**, limit the IP address range to only [New Relic Network blocks for US or EU regions](https://docs.newrelic.com/docs/apm/new-relic-apm/getting-started/networks#webhooks) and consider adding your own authentication mechanism within the script. If you are adding your own authentication you might do this in the payload sent from New Relic Alerts - add a new key in the JSON with a value, and check for that value in the webhook.py script.

Logging is set to at **info** level. Enable **debug** on line 4 to also receive log messages for the full request to New Relic Events API response. By default the info level log will include a new log message when an alert is received without any labels.

**Sample payload (multiple tags)**

```json
{
  "metadata": null,
  "open_violations_count_critical": 0,
  "closed_violations_count_critical": 0,
  "incident_acknowledge_url": "https://alerts.newrelic.com/accounts/12345/incidents/0/acknowledge",
  "targets": [
    {
      "id": "12345",
      "name": "Test Target",
      "link": "http://localhost/sample/callback/link/12345",
      "labels": {
        "label": "value",
        "label2":"value2"
      },
      "product": "TESTING",
      "type": "test"
    }
  ],
  "duration": 1587758775317,
  "open_violations_count_warning": 0,
  "event_type": "NOTIFICATION",
  "incident_id": 0,
  "account_name": "gspncr",
  "details": "New Relic Alert - Channel Test",
  "condition_name": "New Relic Alert - Test Condition",
  "timestamp": 1587758775278,
  "owner": "Gary Spencer",
  "severity": "INFO",
  "policy_url": "https://alerts.newrelic.com/accounts/1147177/policies/0",
  "current_state": "test",
  "policy_name": "New Relic Alert - Test Policy",
  "condition_family_id": null,
  "incident_url": "https://alerts.newrelic.com/accounts/1147177/incidents/0",
  "account_id": 1147177,
  "runbook_url": "http://localhost/runbook/url",
  "violation_chart_url": "http://localhost/sample/violation/charturl/12345",
  "violation_callback_url": "http://localhost/sample/violation/callback/12345",
  "closed_violations_count_warning": 0
}
```