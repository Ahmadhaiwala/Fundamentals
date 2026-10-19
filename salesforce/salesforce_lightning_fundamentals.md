# Salesforce Lightning Fundamentals --- Study Notes

A practical guide to the Salesforce Lightning interface, Lightning
pages, standard components, list views, filters, and the configuration
work you've recently been doing in Trailhead.

## 1. The Salesforce mental model

Salesforce is a CRM platform built around data, user experiences,
automation, and security.

  -----------------------------------------------------------------------
  Salesforce concept      Think of it as          Example
  ----------------------- ----------------------- -----------------------
  Org                     Your Salesforce         Trailhead Playground
                          environment/tenant      

  App                     A workspace with        Sales, Service, Energy
                          navigation and tools    Consultations

  Object                  A database table        Account, Contact,
                                                  Opportunity, Energy
                                                  Audit

  Record                  One row in an object    One customer or one
                                                  opportunity

  Field                   A column/property on a  Stage, Amount, Annual
                          record                  Energy Usage

  Relationship            A link between records  Contact related to an
                                                  Account

  Page                    The UI used to view or  Opportunity record page
                          work with records       

  Component               A reusable UI building  Related Lists, Record
                          block                   Detail, Chatter

  Automation              Logic that runs when    Flow, Apex trigger
                          something happens       
  -----------------------------------------------------------------------

### Standard vs. custom objects

-   **Standard object:** Provided by Salesforce, such as Account,
    Contact, Lead, Opportunity, Product, and Task.
-   **Custom object:** Created for a business-specific need, such as
    `Energy Audit` or `PropertyCopy`.
-   Custom object API names usually end in `__c`; custom field API names
    usually end in `__c`.
-   A **label** is the human-friendly display name; an **API name** is
    used by Salesforce configuration, formulas, SOQL, and code.

### Fields and records

Common field types include Text, Number, Currency, Date, Date/Time,
Checkbox, Picklist, Lookup, and Formula. A field can be marked required,
unique, or have a default value depending on its type and configuration.

## 2. Lightning Experience: the main UI areas

### App navigation

An app groups the tabs users need for a job. The app's navigation bar
can contain objects and tools such as Home, Accounts, Contacts,
Opportunities, Tasks, Chatter, and custom objects.

**Typical setup path:** App Launcher → open the app → use the navigation
bar. To configure an app, go to **Setup → App Manager**, find the app,
and edit its navigation items.

### Setup vs. normal app pages

-   **App pages:** Where users do their day-to-day work.
-   **Setup:** Where admins configure objects, fields, apps, layouts,
    permissions, and automation.
-   **Object Manager:** Setup area for an object's fields,
    relationships, page layouts, compact layouts, buttons, and other
    settings.

## 3. Lightning page types: know the difference

Salesforce uses several kinds of pages. They sound similar, but they
control different things.

  ----------------------------------------------------------------------------
  Page/configuration      What it controls        Example
  ----------------------- ----------------------- ----------------------------
  **Lightning App Page**  A custom page made from A page with reports, lists,
                          Lightning components,   and custom components
                          often for a workspace   
                          or dashboard-like       
                          experience              

  **Lightning Record      The experience when     Opportunity record page
  Page**                  viewing one record      

  **Lightning Home Page** The Home experience for Home page with tasks and
                          an app/profile          dashboards

  **Page Layout**         Fields, buttons,        Opportunity page layout
                          related lists, and      
                          actions in the record   
                          detail experience       

  **Compact Layout**      A small set of key      `New Oppty Compact Layout`
                          fields shown            
                          prominently, especially 
                          in highlights areas and 
                          mobile contexts         

  **List View**           A filtered table of     High Probability
                          many records for an     Opportunities
                          object                  

  **Related List**        Records related to the  Contacts on an Account
                          record currently open   
  ----------------------------------------------------------------------------

**Important:** A Lightning Record Page and a Page Layout are not the
same. The Lightning page controls the overall component arrangement; the
page layout controls much of the record's fields, actions, and
related-list configuration.

## 4. Lightning App Builder and components

**Lightning App Builder** is a drag-and-drop editor for Lightning App,
Home, and Record pages.

### Common page regions

Depending on the page template, you may see regions such as: - Header or
highlights area - Main content area - Sidebars or secondary columns -
Tabs or related-information regions

### Standard Lightning components to recognize

  -----------------------------------------------------------------------
  Component               What it does            Typical use
  ----------------------- ----------------------- -----------------------
  **Record Detail**       Displays record fields  Show the main record
                          according to the        details
                          assigned page layout    

  **Highlights Panel**    Shows key record        Quick view of an
                          information and actions Opportunity
                          at the top              

  **Related Lists**       Shows related records   Contacts,
                                                  Opportunities, or
                                                  related custom records

  **Related List --       Shows one selected      Display only related
  Single**                related list            Contacts

  **Tabs**                Groups content into     Details / Related
                          selectable tabs         

  **Activity**            Shows and supports      Sales activity timeline
                          logging calls, tasks,   
                          and events              

  **Chatter**             Collaboration and feed  Record discussions
                          posts                   

  **Path**                Shows stages and        Opportunity stages
                          guidance for a process  

  **Report Chart**        Embeds a report chart   Visualize pipeline data
                          on a page               

  **List View**           Shows a list of object  A work queue
                          records                 

  **Rich Text**           Displays formatted text Page guidance
                          or instructions         

  **Dashboard**           Displays dashboard      KPI overview
                          information where       
                          supported               

  **Flow**                Embeds a screen flow in Guided data entry
                          a page                  

  **Visualforce**         Embeds a Visualforce    Legacy/custom UI
                          page                    

  **Custom Lightning Web  Displays a              Specialized
  Component**             developer-built         functionality
                          component               
  -----------------------------------------------------------------------

Available components depend on the page type, Salesforce edition,
permissions, and the configuration of your org.

### Typical page-building workflow

1.  Open **Setup → Lightning App Builder**.
2.  Create a new page or open an existing page.
3.  Choose a page type and template.
4.  Drag components into the available regions.
5.  Configure each component's properties.
6.  Save.
7.  Activate the page and assign it to the appropriate app, record type,
    profile, or form factor as needed.
8.  Test as a normal user, not only as an administrator.

### Activation and assignment

Saving a page does not necessarily make it the active page for everyone.
Activation controls where the page is used. Check the assignment scope
carefully: org default, app default, app/profile, or
record-type-specific assignments may affect what users see.

## 5. List views: your recent Trailhead work

A **list view** is a saved way to display a subset of records from one
object. It normally has columns, filters, and a visibility setting.

Examples: - Recently Viewed Opportunities - My Open Opportunities - High
Probability Opportunities - Energy Audits needing review

### Create or edit a list view

1.  Open the relevant object tab, such as **Opportunities**.
2.  Open the list-view selector.
3.  Choose **New** or edit an existing list view.
4.  Enter a display label and, where required, a list-view name/API
    name.
5.  Choose who can see it: only you, a group, or all users (options
    depend on permissions).
6.  Add filters.
7.  Select the columns to display.
8.  Save, then confirm the resulting records match the intended
    criteria.

### Columns vs. filters

-   **Columns** control what information appears in the table.
-   **Filters** control which records appear in the table.
-   Changing a column does not change which records qualify.
-   Changing a filter does not automatically add a useful column to
    display.

### List-view controls to recognize

-   Search within the list
-   Refresh
-   Select and reorder columns
-   Sort by a column
-   Filter by field values
-   List-view charts, when available
-   Actions such as New, Edit, Delete, or other object-specific actions,
    depending on permissions

## 6. Filters and Filter Logic --- especially important

Each filter is assigned a number. You can then combine the numbered
filters using **Filter Logic**.

### Example: High Probability Opportunities

Goal: show opportunities whose Stage is either **Proposal/Price Quote**
or **Negotiation/Review**, and whose Probability is at least 50%.

Create these filters:

  Filter number   Field         Operator                   Value
  --------------- ------------- -------------------------- ----------------------
  1               Stage         equals                     Proposal/Price Quote
  2               Stage         equals                     Negotiation/Review
  3               Probability   greater than or equal to   50

Then set **Filter Logic** to:

``` text
(1 OR 2) AND 3
```

Meaning: - Filter 1 or filter 2 must match. - Filter 3 must also
match. - So the stage must be one of the two specified stages **and**
probability must be 50% or higher.

**Do not put `(1 OR 2) AND 3` into the Probability filter's Value box.**
Filter Logic is a separate setting from the individual filter
field/operator/value controls.

### Logic patterns

Assume: - 1 = Stage is Proposal - 2 = Stage is Negotiation - 3 =
Probability is at least 50 - 4 = Owner is me

  -----------------------------------------------------------------------
  Filter Logic                        Meaning
  ----------------------------------- -----------------------------------
  `1 AND 2`                           Both 1 and 2 must be true

  `1 OR 2`                            Either 1 or 2 can be true

  `(1 OR 2) AND 3`                    Either stage condition, and
                                      probability must also qualify

  `(1 OR 2) AND (3 OR 4)`             One of filters 1/2, and one of
                                      filters 3/4

  `1 AND 2 AND 3`                     All three conditions must be true

  `1 OR 2 OR 3`                       Any one of the three conditions can
                                      be true

  `1 AND (2 OR 3)`                    Filter 1 is required; either 2 or 3
                                      must also match
  -----------------------------------------------------------------------

### How to build logic with three conditions

If the requirement says **condition A OR condition B OR condition C**,
create three separate filters and enter:

``` text
1 OR 2 OR 3
```

If it says **A or B, but C must always be true**, enter:

``` text
(1 OR 2) AND 3
```

If it says **A must be true, and either B or C**, enter:

``` text
1 AND (2 OR 3)
```

### A quick translation method

Translate the sentence before configuring: - "and" usually maps to
`AND`. - "or" usually maps to `OR`. - "must also," "only if," or "in
addition to" often signals an `AND`. - Parentheses group conditions so
they are evaluated together.

Create the individual filters first, then write logic using their
numbers. Check that the logic references only existing filter numbers.

### Common filter mistakes

-   Using the wrong operator (`equals` instead of
    `greater than or equal to`).
-   Entering a percentage incorrectly; use the value format the filter
    UI expects.
-   Putting filter logic into a filter's Value field.
-   Forgetting parentheses when conditions must be grouped.
-   Choosing the wrong visibility setting.
-   Assuming a filter controls table columns.
-   Not checking whether the chosen fields are available in that
    object's list-view filters.

## 7. List View Charts

A list-view chart summarizes the records in the selected list view. It
is a visualization of the records that qualify for that view; it is not
a replacement for the filters.

### Your recent chart example

For the **High Probability Opportunities** list: - Chart type:
**Donut** - Aggregate/measure: **Sum of Amount** - Grouping: **Account
Name**

The chart then shows the distribution of opportunity Amount by Account
Name for records included in the list view.

### Chart setup checklist

1.  Open the list view.
2.  Open the chart panel or chart controls.
3.  Create or edit a chart.
4.  Select a chart type.
5.  Choose the aggregate measure (for example, Sum of Amount).
6.  Choose the grouping field (for example, Account Name).
7.  Save and check whether the chart communicates the intended
    comparison.

**Tip:** A chart is only as useful as the list view and grouping field
behind it. If the filters exclude records, the chart won't include them.

## 8. Compact Layouts, Highlights Panel, and Page Layouts

These three are related, but they do different jobs.

### Compact Layout

-   Defines a small set of important fields for quick scanning.
-   Has a label and API name.
-   On Opportunity, you recently worked with:
    -   Label: `New Oppty Compact Layout`
    -   API name: `New_Oppty_Compact_Layout`

### Highlights Panel

-   A Lightning page component that displays key information and actions
    near the top of a record page.
-   The compact layout helps determine which fields appear in the
    highlights area.

### Page Layout

-   Controls much of the record detail experience, including field
    placement, buttons/actions, and related lists.
-   Different profiles or record types may use different page layouts.

### Typical configuration path

**Setup → Object Manager → Opportunity → Compact Layouts** to
create/edit a compact layout. Then check the object's **Compact Layout
Assignment** if you need to control which one is primary.

For page layouts, use **Setup → Object Manager → Opportunity → Page
Layouts**.

## 9. Feed Tracking and Chatter

Feed Tracking makes selected field changes visible in an object's feed,
where supported. It is different from simply displaying a field on a
page.

In your Energy Audit task, the fields to enable tracking were: -
Account - Audit Notes - Energy Audit Name - Type of Installation -
Annual Energy Usage (kWh) - Average Annual Electric Cost

Typical path: **Setup → Feature Settings / Chatter settings → Feed
Tracking** (the exact navigation can vary) → choose the object → enable
tracking → select the fields → save.

Checklist: - Confirm Feed Tracking is enabled for the object. - Confirm
each required field is selected. - Save. - Recheck the Trailhead
challenge; exact field selection matters.

## 10. Custom objects and fields: fundamentals

A custom object lets an organization store data that doesn't fit a
standard object.

Example: a custom `PropertyCopy` object with a required Currency field
`PriceCopy`.

### Basic setup flow

1.  Go to **Setup → Object Manager → Create → Custom Object**.
2.  Enter the label and object name.
3.  Configure optional settings such as record name and reporting, as
    appropriate.
4.  Save.
5.  Open **Fields & Relationships → New**.
6.  Choose a field type, such as Currency.
7.  Set the label/API name and field options.
8.  Mark it required if every record must have a value.
9.  Add it to the relevant page layout if needed.
10. Create a test record and verify the field behaves as expected.

### Object relationships

-   **Lookup relationship:** A flexible link between records; the child
    record can often exist without the related parent, depending on
    configuration.
-   **Master-detail relationship:** A tighter parent-child relationship
    with inherited sharing behavior and roll-up summary support on the
    master, subject to Salesforce rules.
-   Choose a relationship based on the actual business rule, not merely
    because two objects are connected.

## 11. Object Manager vs. Lightning App Builder vs. App Manager

  -----------------------------------------------------------------------
  Tool                                Use it for
  ----------------------------------- -----------------------------------
  **Object Manager**                  Objects, fields, relationships,
                                      page layouts, compact layouts,
                                      record types, and object settings

  **Lightning App Builder**           Arrange components on Lightning
                                      Home, App, and Record pages

  **App Manager**                     Create/edit apps, navigation items,
                                      branding, and app settings

  **List View controls**              Configure a saved record list,
                                      filters, columns, and charts

  **Setup → Feed Tracking**           Choose which field changes appear
                                      in feeds
  -----------------------------------------------------------------------

A useful debugging question is: **"What exactly am I trying to
change?"** - A field's definition? Object Manager. - The arrangement of
components on a record page? Lightning App Builder. -
Fields/buttons/related lists in the record detail layout? Page Layout. -
The app's navigation tabs? App Manager. - Which records appear in a
table? List View filters. - Which fields are prominent at the top?
Compact Layout / Highlights Panel. - Which field changes show in a feed?
Feed Tracking.

## 12. Security and visibility basics

Salesforce visibility can be affected by several layers: - **Object
permissions:** Can the user read/create/edit/delete records of this
object? - **Field-level security (FLS):** Can the user see or edit a
particular field? - **Record-level access:** Can the user access this
specific record? - **Page/app assignment:** Is the right page or app
assigned to this user? - **List-view visibility:** Who can open the
saved list view?

A list view set to "all users" does not automatically grant access to
every record. Salesforce permissions and record sharing still apply.

## 13. A practical troubleshooting checklist

When a Trailhead challenge says the setup is incorrect:

1.  Re-read the exact required **label** and **API name**.
2.  Check that you're working in the correct Playground/org.
3.  Verify the correct object is selected.
4.  Compare every filter's field, operator, and value.
5.  Verify Filter Logic separately from individual filter values.
6.  Check the required columns and their order if specified.
7.  Confirm list-view visibility.
8.  For charts, verify type, aggregate, and grouping field.
9.  For compact layouts, verify the fields and compact layout
    assignment.
10. For Feed Tracking, confirm both the object and every required field.
11. Save changes, refresh, and rerun the challenge.
12. If it still fails, inspect for a similarly named duplicate
    configuration.

## 14. Quick glossary

-   **Lightning Experience:** Salesforce's modern browser UI.
-   **Lightning App Builder:** Drag-and-drop editor for Lightning pages.
-   **Lightning component:** A reusable UI element.
-   **Record page:** UI for an individual record.
-   **Page layout:** Configuration for record details, actions, and
    related lists.
-   **Compact layout:** Small set of prominent record fields.
-   **List view:** Saved filtered table of records.
-   **Filter logic:** Boolean expression combining numbered list-view
    filters.
-   **List-view chart:** Chart based on the records in a list view.
-   **API name:** Stable identifier used by configuration and code.
-   **Chatter feed:** Collaboration stream that can show posts and
    tracked field changes.
-   **Trailhead Playground:** A Salesforce environment used for hands-on
    learning.

## 15. Mini practice exercises

Try solving these without looking at the answers first.

### Exercise A

Show Opportunities where Stage is Proposal **or** Negotiation, and
Amount is greater than 100,000.

Filters: 1. Stage equals Proposal 2. Stage equals Negotiation 3. Amount
greater than 100000

Filter Logic:

``` text
(1 OR 2) AND 3
```

### Exercise B

Show records where Status is New, Working, **or** Escalated.

Filters: 1. Status equals New 2. Status equals Working 3. Status equals
Escalated

Filter Logic:

``` text
1 OR 2 OR 3
```

### Exercise C

Show Opportunities owned by me, with either Stage = Proposal or
Probability \>= 70%.

Filters: 1. Owner equals me 2. Stage equals Proposal 3. Probability
greater than or equal to 70

Filter Logic:

``` text
1 AND (2 OR 3)
```

### Exercise D

You want the Opportunity's key fields near the top of the record, but
you do not want to rearrange the entire record detail section. What
should you check?

**Answer:** The Compact Layout assignment used by the Highlights Panel.

### Exercise E

You want to change the navigation tabs in the Energy Consultations app.
Which tool should you use?

**Answer:** App Manager.

### Exercise F

You want to show only certain records in a table, without changing the
object's field definitions. What should you configure?

**Answer:** A List View and its filters.

------------------------------------------------------------------------

## Suggested learning order

1.  Objects, fields, records, and standard vs. custom objects.
2.  Apps, navigation, and Setup.
3.  List views: columns, sorting, filters, visibility.
4.  Filter Logic: `AND`, `OR`, and parentheses.
5.  List-view charts.
6.  Page layouts vs. compact layouts vs. Lightning Record Pages.
7.  Lightning App Builder and standard components.
8.  Object relationships.
9.  Chatter and Feed Tracking.
10. After these admin fundamentals, move into Flow, SOQL, Apex, and
    Lightning Web Components (LWC).

**Core takeaway:** Salesforce has separate tools for data structure,
record layout, page composition, navigation, and record filtering.
Identify which layer controls the behavior you want to change before
editing anything.
