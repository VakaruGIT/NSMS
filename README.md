# A Newspaper Subscription Management Software
## Functionality

The API consists of the following main functionality

**Management of newspapers and issues**
- Add/remove/update a new newspaper. Each paper has a (unique) paper ID, name, issue frequency (in days), and monthly price
- Add/remove/update an issue of a newspaper. Each issue has a publication date, number of pages, etc
- Each issue has an editor (i.e. the responsible person; see below)
- Initially, paper issues are not published, but once updated, they can be delivered to subscribers

**Management of editors**
- Add/remove/update editors to/from the system. Each editor has a (unique) editor-id, name, address and a list of newspapers, s/he can work for care of.
- When an editor is removed (e.g., quits the job), transfer all issues in his/her supervision to another editor of the same newspaper.

**Management of subscribers**
- Add/remove subscribers to/from the system. Each subscriber has a (unique) subscriber ID, name, address and a list of newspapers that they are subscribed to.
- Each client can choose to subscribe to special issues
- When a client is removed (e.g., cancels a subscription), all subscriptions are stopped



| Endpoint                                         | HTTP Method | Description                                                                                                                                             |
|--------------------------------------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `/newspaper`                                     | `GET`       | List all newspapers in the agency.                                                                                                                      |
| `/newspaper`                                     | `POST`      | Create a new newspaper.                                                                                                                                 |
| `/newspaper/<paper_id>`                          | `GET`       | Get a newspaper's information.                                                                                                                          |
| `/newspaper/<paper_id>`                          | `POST`      | Update a new newspaper.                                                                                                                                 |
| `/newspaper/<paper_id>`                          | `DELETE`    | Delete a newspaper, and all its issues.                                                                                                                 |
| `/newspaper/<paper_id>/issue`                    | `GET`       | List all issues of a specific newspaper.                                                                                                                |
| `/newspaper/<paper_id>/issue`                    | `POST`      | Create a new issue.                                                                                                                                     |
| `/newspaper/<paper_id>/issue/<issue_id>`         | `GET`       | Get information of a newspaper issue                                                                                                                    |
| `/newspaper/<paper_id>/issue/<issue_id>/release` | `POST`      | Release an issue                                                                                                                                        |
| `/newspaper/<paper_id>/issue/<issue_id>/editor`  | `POST`      | Specify an editor for an issue. (Transmit the editor ID as parameter)                                                                                   |
| `/newspaper/<paper_id>/issue/<issue_id>/deliver` | `POST`      | "Send" an issue to a subscriber. This means there should be a record of the subscriber receiving                                                        |
| `/newspaper/<paper_id>/stats`                    | `GET`       | Return information about the specific newspaper (number of subscribers, monthly and annual revenue)                                                     |
| `/editor`                                        | `GET`       | List all editors of the agency.                                                                                                                         |
| `/editor`                                        | `POST`      | Create a new editor.                                                                                                                                    |
| `/editor/<editor_id>`                            | `GET`       | Get an editor's information.                                                                                                                            |
| `/editor/<editor_id>`                            | `POST`      | Update an editor's information.                                                                                                                         |
| `/editor/<editor_id>`                            | `DELETE`    | Delete an editor.                                                                                                                                       |
| `/editor/<editor_id>/issues`                     | `GET`       | Return a list of newspaper issues that the editor was responsible for.                                                                                  |
| `/subscriber`                                    | `GET`       | List all subscribers in the agency.                                                                                                                     |
| `/subscriber`                                    | `POST`      | Create a new subscriber.                                                                                                                                |
| `/subscriber/<subscriber_id>`                    | `GET`       | Get a subscriber's information.                                                                                                                         |
| `/subscriber/<subscriber_id>`                    | `POST`      | Update a subscriber's information.                                                                                                                      |
| `/subscriber/<subscriber_id>`                    | `DELETE`    | Delete a subscriber.                                                                                                                                    |
| `/subscriber/<subscriber_id>/subscribe`          | `POST`      | Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as parameter.)                                                                        |
| `/subscriber/<subscriber_id>/stats`              | `GET`       | Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper. |
| `/subscriber/<subscriber_id>/missingissues`      | `GET`       | Check if there are any undelivered issues of the subscribed newspapers.                                                                                 |
---

### Installation

You should not need any packages beyond those in [requirements.txt](./requirements.txt) 
to get started.

### Run the webserver

You can start the app by executing
```bash
python start.py
```

Then, you can navigate to http://127.0.0.1:7890/ and try the endpoints using the Swagger interface.

### Testing with [pytest](https://docs.pytest.org/)

To trigger the automated tests, execute
```bash
pytest
```

Note, that your `print` statements will not be visible, 
unless you add the `-s` argument to the call, i.e. `pytest -s`.
