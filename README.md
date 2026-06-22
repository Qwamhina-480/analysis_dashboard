# Sugar Trap: Finding the Blue Ocean in Healthy Snacking

## A. Executive Summary

This project analyzes snack products from the Open Food Facts dataset to identify underserved opportunities in the healthy snacking 
market. After cleaning the data and grouping products into high-level snack categories, I created a Nutrient Matrix comparing 
sugar and protein content across categories. The analysis showed that the High Protein–Low Sugar segment is dominated by Nuts & Seeds,
while Snack Bars are significantly underrepresented. Based on the findings, the strongest market opportunity is a low-sugar, 
high-protein Snack Bar with at least 10g protein and less than 5g sugar per 100g.

## B. Project Links

**GitHub Repository:**
https://github.com/Qwamhina-480/analysis_dashboard

**Interactive Dashboard:**
https://analysisdashboard-hnz3daowkhjbpcn9jog9n9.streamlit.app/

**Notebook:**
https://colab.research.google.com/drive/1mRtWO-02Z3imYib9elIm4Jj5n7l2JP8k?usp=sharing

**Presentation:**
https://docs.google.com/presentation/d/1br5oCZuKjZb8oPFgtya_BWSFVVhygD5fMXD9uaUdLSA/edit?usp=sharing

## C. Technical Explanation

### Data Cleaning

The original Open Food Facts dataset was large, so I selected only the columns relevant to the business problem: product name, 
category tags, ingredients, sugar, protein, fat, fiber, Nutri-Score, and NOVA group. Rows with missing critical fields such as 
product name, sugar, protein, or category tags were removed. Nutritional outliers were filtered by keeping biologically realistic
values between 0g and 100g per 100g.

### Category Engineering

The `categories_tags` column contained many detailed and messy product tags. I first explored the most common tags, then created
a snack-focused dataset using snack-related keywords. Products were grouped into business-friendly categories: Sweet Snacks, 
Breakfast & Cereal Snacks, Nuts & Seeds, Salty Snacks, Snack Bars, General / Unspecified Snacks, and Biscuits & Cookies.

### Nutrient Matrix

The Nutrient Matrix compared sugar content against protein content. I defined the target healthy-snacking zone as products with
at least 10g protein and no more than 5g sugar per 100g. This helped identify which categories already serve the healthy snack
market and which categories are underserved.

### Key Finding

The High Protein–Low Sugar zone contained 1,657 products, but most were Nuts & Seeds. Snack Bars had only 35 products in this
target zone, showing that this category is underrepresented despite being a convenient and popular snack format.

### Candidate’s Choice Addition

I added a Health Opportunity Score to provide an extra business metric. The score rewards higher protein and fiber while 
penalizing sugar and fat. This helps compare snack categories beyond the basic sugar-protein scatter plot.

## Final Recommendation

Based on the data, the biggest market opportunity is in **Snack Bars**, specifically targeting products with:

* Protein ≥ 10g per 100g
* Sugar ≤ 5g per 100g
* Portable snack-bar format
* Nutritional positioning similar to Nuts & Seeds, but with greater convenience

