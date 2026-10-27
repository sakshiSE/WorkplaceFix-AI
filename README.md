# WorkplaceFix AI
### From Employee Feedback to Practical Workplace Improvements

## 1. About the Project

WorkplaceFix AI is an interactive website that helps users explore job satisfaction and identify recurring workplace concerns from employee feedback.

The project is based on the article *“When The Pay Was Terrible, But The Friendships Priceless”*, which highlights four factors affecting job satisfaction:

- What you do
- How much you earn
- Where you work
- Who you work with

The website connects these factors with feedback analysis and practical workplace improvement suggestions.

## 2. Problem Statement

Employee feedback may contain useful information about salary, workload, management, career growth and workplace relationships. Manually reviewing many comments can make recurring concerns difficult to identify.

WorkplaceFix AI organises feedback into themes and presents the findings in an interactive dashboard to support further discussion and action planning.

## 3. Features

- **Four-factor model:** Explains the main factors affecting job satisfaction.
- **Self-assessment:** Lets users rate their satisfaction with the four factors.
- **CSV upload:** Allows users to upload and preview feedback data.
- **Theme detection:** Groups feedback using predefined keyword rules.
- **Interactive dashboard:** Displays metrics, charts and summary tables.
- **Feedback exploration:** Shows example comments associated with selected themes.
- **Improvement suggestions:** Connects recognised themes to possible actions.
- **Action tracker:** Helps organise suggested owners, timeframes, progress measures and status.
- **Report downloads:** Exports analysis results as CSV and Excel files.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Pandas | Data processing and analysis |
| Regular expressions | Keyword matching |
| HTML and CSS | Website styling |
| OpenPyXL | Excel report generation |

## 5. How It Works

1. Open the website.
2. Read the four-factor explanation or complete the self-assessment.
3. Select built-in demonstration data or upload a CSV file.
4. Preview the data.
5. Click **Analyse feedback** after uploading a CSV.
6. Explore the identified themes and supporting feedback examples.
7. Review the suggested workplace improvements.
8. Create an action tracker and download the report.

## 6. Installation and Execution

### Requirements

Install Python on your computer. Python 3.10 or later is recommended.

Open a terminal inside the project folder and run:

```bash
python -m pip install -r requirements.txt
```

Start the website:

```bash
python -m streamlit run website_app_revised.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`. Open it in your browser.

## 7. Input Data

The application accepts CSV files containing at least one suitable text column, such as:

- `feedback`
- `comments`
- `review`
- `text`
- `Likes`
- `Dislikes`

Numeric rating columns may also be included. The website attempts to recognise suitable text and rating columns.

## 8. Analysis Method

The current version uses predefined keywords to identify workplace themes. It counts the distinct feedback records mentioning each theme and calculates their percentage of the analysed records.

The application then connects recognised themes to predefined workplace improvement suggestions.

This is a rule-based text-analysis approach. It is not a trained machine-learning model and does not reliably understand sentiment, sarcasm, context or negation.

## 9. Responsible Use

- Remove names, email addresses and other identifying details before uploading data.
- Upload only feedback you are authorised to use.
- Treat findings as patterns in the supplied dataset, not proof of causes.
- Review recommendations in the context of the workplace.
- Do not use the results to automatically rank, penalise or make employment decisions about individuals.

The built-in demonstration data is fictional.

## 10. Limitations and Future Improvements

Keyword matching may miss relevant feedback or misinterpret comments. Future improvements could include a trained sentiment-analysis model, better handling of context, evaluation against manually labelled feedback and additional trend analysis.

## 11. Assignment Context

**Assignment:** Assignment F — Job Satisfaction and Workplace Wellbeing  
**Project:** WorkplaceFix AI  
**Track:** AI Engineering / Issue-Focused Website

The project demonstrates how an interactive website and basic data analysis can help users explore workplace wellbeing and organise possible improvements.
