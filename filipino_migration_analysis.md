
# Rey's Sample Works - Filipino Migration

<a href=""><img src="https://img.shields.io/badge/HOME%20GitHub-0068cb" /></a>

---
## Links:

### Dashboard
- [Tableau - Filipino Migration](https://public.tableau.com/app/profile/rey.lawrence.torrecampo/viz/LinangSP801-Dashboard/AvgMigrationforCountryandTrend)

### Powerpoint Presentation

- [Analysis Deck](https://docs.google.com/presentation/d/1lnjEUYQPrJt_RHJsBDATLCiE0famsivh/edit?usp=sharing&ouid=110356754673487953492&rtpof=true&sd=true)
    + Go to this file for full presentation
    + Other documents are process of cleaning the data

### Excel File Analyzing the data
- [Supporting Analysis Part 1](https://docs.google.com/spreadsheets/d/1qSgIro4rBF1l0bAty_pEwyPKw-_c9S4R/edit?usp=sharing&ouid=110356754673487953492&rtpof=true&sd=true)


- [Supporting Analysis Part 2](https://docs.google.com/spreadsheets/d/1x5KlGA22SgBT3PzuLcavqkIrAj6Msnc1/edit?usp=sharing&ouid=110356754673487953492&rtpof=true&sd=true)

- [Unpivotted Data](https://drive.google.com/file/d/1RnZ3wUb3O4aEVxjnmwCnxHnIWDDEHv48/view?usp=sharing)

---

## Visualization Sample

<div class='tableauPlaceholder' id='viz1712186862474' style='position: relative'>
  <noscript>
    <a href='#'>
      <img alt='Average Number of Filipinos Migrating to their Designated Country of Choice for Ages between 20 to 69 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Li&#47;LinangSP801-Dashboard&#47;AvgMigrationforCountryandTrend&#47;1_rss.png' style='border: none' />
    </a>
  </noscript>
  <object class='tableauViz' style='display:none;'>
    <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    <param name='embed_code_version' value='3' />
    <param name='site_root' value='' />
    <param name='name' value='LinangSP801-Dashboard&#47;AvgMigrationforCountryandTrend' />
    <param name='tabs' value='no' />
    <param name='toolbar' value='yes' />
    <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Li&#47;LinangSP801-Dashboard&#47;AvgMigrationforCountryandTrend&#47;1.png' />
    <param name='animate_transition' value='yes' />
    <param name='display_static_image' value='yes' />
    <param name='display_spinner' value='yes' />
    <param name='display_overlay' value='yes' />
    <param name='display_count' value='yes' />
    <param name='language' value='en-US' />
  </object>
</div>
<script type='text/javascript'>
  var divElement = document.getElementById('viz1712186862474');
  var vizElement = divElement.getElementsByTagName('object')[0];
  if (divElement.offsetWidth > 800) {
    vizElement.style.minWidth = '600px';
    vizElement.style.maxWidth = '1800px';
    vizElement.style.width = '100%';
    vizElement.style.minHeight = '747px';
    vizElement.style.maxHeight = '1227px';
    vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
  } else if (divElement.offsetWidth > 500) {
    vizElement.style.minWidth = '600px';
    vizElement.style.maxWidth = '1800px';
    vizElement.style.width = '100%';
    vizElement.style.minHeight = '747px';
    vizElement.style.maxHeight = '1227px';
    vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
  } else {
    vizElement.style.width = '100%';
    vizElement.style.height = '1677px';
  }
  var scriptElement = document.createElement('script');
  scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
  vizElement.parentNode.insertBefore(scriptElement, vizElement);
</script>

---
## Unpivoting Tables
Data set is currently pivotted. In order to properly, analyze it, it was loaded in SQL Server and unpivotted.
To unpivot the tables, the original data set is saved in a temporary table then loaded to a real table.

### Save Unpivoting Tables to Temporary Tables
#### Regions
```
    SELECT [year], [Region], migration_numbers into ##regions
    FROM   
    (SELECT [year], Region_I,Region_II ,Region_III,Region_IV_A,Region_IV_B,Region_V,Region_VI,Region_VII,Region_VIII,Region_IX,Region_X,Region_XI,Region_XII,Region_XIII, cast(ARMM as smallint) as ARMM,CAR,NCR
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [Region] IN   
        (Region_I,Region_II ,Region_III,Region_IV_A,Region_IV_B,Region_V,Region_VI,Region_VII,Region_VIII,Region_IX,Region_X,Region_XI,Region_XII,Region_XIII,ARMM,CAR,NCR)  
        )AS unpvt;
```
#### Educational Level
```
    SELECT [year], [education_level], migration_numbers into ##education_level
    FROM   
    (SELECT [year], No_Education,Primary_Education,Secondary_Education,try_cast(Post_Secondary as smallint) as Post_Secondary,Post_Graduate
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [education_level] IN   
        (No_Education,Primary_Education,Secondary_Education,Post_Secondary,Post_Graduate)  
        )AS unpvt;  
```
####  Major_countries
```
    SELECT [year], [major_destination], migration_numbers into ##major_destination
    FROM   
    (SELECT [year],USA,CANADA,cast(JAPAN as int) as JAPAN, cast(AUSTRALIA as int) as AUSTRALIA, cast(ITALY as int) ITALY, cast(NEW_ZEALAND as int) NEW_ZEALAND, cast(UNITED_KINGDOM as int) UNITED_KINGDOM, cast(GERMANY as int) as GERMANY, cast(SOUTH_KOREA as int) as SOUTH_KOREA, cast(SPAIN as int) as SPAIN, cast(OTHERS as int) as OTHERS
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [major_destination] IN   
        (USA,CANADA,JAPAN,AUSTRALIA,ITALY,NEW_ZEALAND,UNITED_KINGDOM,GERMANY,SOUTH_KOREA,SPAIN,OTHERS)  
        )AS unpvt;  
```
####  Age Groups
```
    SELECT [year], [age_group], migration_numbers into ##age_group
    FROM   
    (SELECT [year],_14_Below,_15_19,_20_24,_25_29,_30_34,_35_39,_40_44,_45_49,_50_54,_55_59,_60_64,_65_69,_70_Above
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [age_group] IN   
        (_14_Below,_15_19,_20_24,_25_29,_30_34,_35_39,_40_44,_45_49,_50_54,_55_59,_60_64,_65_69,_70_Above)  
        )AS unpvt;  

        --- sex unpivot ----
    SELECT [year], [sex], migration_numbers into ##sex
    FROM   
    (SELECT [year], MALE, FEMALE
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [sex] IN   
        (MALE, FEMALE)  
        )AS unpvt;  
```

####  Marital Status
```
    SELECT [year], [marital_status], migration_numbers into ##marital_status
    FROM   
   (SELECT [year], Single, Married, cast(Widower as int) Widower, cast(Separated as int) Separated, cast(Divorced as int) as Divorced
   FROM to_unpivot) p  
    UNPIVOT  
   (migration_numbers FOR [marital_status] IN   
      (Single, Married, Widower, Separated, Divorced)  
	)AS unpvt;  
```

####  Occupution
```
    SELECT [year], [occupation], migration_numbers into ##occupation
    FROM   
    (SELECT [year], Prof_l_Tech_l_Related_Workers, Administrative_Workers, Clerical_Workers, Sales_Workers, Service_Workers ,Workers_Fishermen ,Equipment_Operators_Laborers ,Members_of_the_Armed_Forces ,Housewives ,Retirees ,Students ,Minors_Below_7_years_old ,Out_of_School_Youth ,cast(Refugees as smallint) as  Refugees,No_Occupation_Reported
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [occupation] IN   
        (Prof_l_Tech_l_Related_Workers, Administrative_Workers, Clerical_Workers, Sales_Workers, Service_Workers ,Workers_Fishermen ,Equipment_Operators_Laborers ,Members_of_the_Armed_Forces ,Housewives ,Retirees ,Students ,Minors_Below_7_years_old ,Out_of_School_Youth ,Refugees ,No_Occupation_Reported)  
        )AS unpvt;  
```

####  Occupution
```
    SELECT [year], [occupation], migration_numbers into ##occupation
    FROM   
    (SELECT [year], Prof_l_Tech_l_Related_Workers, Administrative_Workers, Clerical_Workers, Sales_Workers, Service_Workers ,Workers_Fishermen ,Equipment_Operators_Laborers ,Members_of_the_Armed_Forces ,Housewives ,Retirees ,Students ,Minors_Below_7_years_old ,Out_of_School_Youth ,cast(Refugees as smallint) as  Refugees,No_Occupation_Reported
    FROM to_unpivot) p  
    UNPIVOT  
    (migration_numbers FOR [occupation] IN   
        (Prof_l_Tech_l_Related_Workers, Administrative_Workers, Clerical_Workers, Sales_Workers, Service_Workers ,Workers_Fishermen ,Equipment_Operators_Laborers ,Members_of_the_Armed_Forces ,Housewives ,Retirees ,Students ,Minors_Below_7_years_old ,Out_of_School_Youth ,Refugees ,No_Occupation_Reported)  
        )AS unpvt;  
```

----

### Save Unpivoting Tables to Temporary Tables

#### Create Unpivoted Table
```
    create table dbo.unpivoted_migration_numbers (
        year int
        --, total_migration_numbers int
        , region varchar(100)
        , education_level varchar(100)
        , major_destination varchar(100)
        , sex varchar(100)
        , age_group varchar(100)
        , marital_status varchar(100)
        , employment_status varchar(100)
        , migration_numbers int
    )
```
#### Loading Data to Real Table
```
    insert into dbo.unpivoted_migration_numbers(
        [year]
        , region
        , sex
        , marital_status
        , education_level
        , major_destination
        , age_group
        , employment_status
        , migration_numbers
    )

    SELECT
    A.[year]
    , A.[Region]
    , B.[sex]
    , C.[marital_status]
    , D.[education_level]
    , E.major_destination
    , F.age_group
    , G.employment_status
    , cast(round(A.migration_numbers * migration_percentage_sex * migration_percentage_marital_status * migration_percentage_education_level * migration_percentage_major_dest * migration_percentage_age_group * migration_percentage_employment, 0) as int) as migration_numbers
    from ##regions A
    left join (
        select 
        [year]
        , [sex]
        , cast(migration_numbers as decimal(8,2)) / sum(migration_numbers) over (partition by [year] order by [year] asc) as migration_percentage_sex
        from ##sex
    ) B on A.[year] = B.[year]
    left join (
        select 
        [year]
        , [marital_status]
        , cast(migration_numbers as decimal(8,2)) / sum(migration_numbers) over (partition by [year] order by [year] asc) as migration_percentage_marital_status
        from ##marital_status
    ) C on A.[year] = C.[year]
    left join (
        select 
        [year]
        , [education_level]
        , cast(migration_numbers as decimal(8,2)) / sum(migration_numbers) over (partition by [year] order by [year] asc) as migration_percentage_education_level
        from  ##education_level
    ) D on A.[year] = D.[year]
    left join (
        select 
        [year]
        , [major_destination]
        , cast(migration_numbers as decimal(8,2)) / sum(migration_numbers) over (partition by [year] order by [year] asc) as migration_percentage_major_dest
        from  ##major_destination
    ) E on A.[year] = E.[year]
    left join (
        select 
        [year]
        , [age_group]
        , cast(migration_numbers as decimal(8,2)) / sum(migration_numbers) over (partition by [year] order by [year] asc) as migration_percentage_age_group
        from  ##age_group
    ) F on A.[year] = F.[year]
    left join (
        select 
        [year]
        , [employment_status]
        , cast(migration_numbers as decimal(8,2)) / sum(migration_numbers) over (partition by [year] order by [year] asc) as migration_percentage_employment
        from  ##employment
    ) G on A.[year] = G.[year]
    where cast(round(A.migration_numbers * migration_percentage_sex * migration_percentage_marital_status * migration_percentage_education_level * migration_percentage_major_dest * migration_percentage_age_group * migration_percentage_employment, 0) as int) > 0

```
#### Cleaned Real Table

```
    create table dbo.unpivoted_migration_numbers_cleaned (
        year int
        , region varchar(100)
        , region_code int
        , education_level varchar(100)
        , education_level_code int
        , major_destination varchar(100)
        , major_destination_code int
        , sex varchar(100)
        , sex_code int
        , age_group varchar(100)
        , age_group_code int
        , marital_status varchar(100)
        , marital_status_code int
        , employment_status varchar(100)
        , employment_status_code int
        , migration_numbers int
    )
```

### Loading Table to Real Table

```
    insert into dbo.unpivoted_migration_numbers_cleaned (
        [year]
        , region
        , region_code
        , education_level
        , education_level_code
        , major_destination
        , major_destination_code
        , sex
        , sex_code
        , age_group
        , age_group_code
        , marital_status
        , marital_status_code
        , employment_status
        , employment_status_code
        , migration_numbers
    )
    select
        [year]
        , A.region
        , REG.code as region_code
        , education_level
        , EDU.code as educational_level_code
        , major_destination
        , DEST.code as major_destination_code
        , sex
        , SEX.code as sex_code
        , age_group
        , AGE.code as age_group_code
        , marital_status
        , MAR.code as marital_status_code
        , employment_status
        , EMP.code as employment_status_code
        , migration_numbers
    from (
    select
        --ROW_NUMBER() over (order by [year]) - 1800
        [year]
        , replace(region, '_', ' ') as region
        , replace(education_level, '_', ' ') as education_level
        , replace(major_destination, '_', ' ') as major_destination
        , upper(left(sex, 1)) + lower(right(sex, len(sex) - 1)) as sex
        , case when 
        coalesce(try_cast(left(trim(right(age_group, len(age_group) - 1)),2) as int),0) between 15 and 69 then replace(trim(right(age_group, len(age_group) - 1)), '_' ,' to ')
        else replace(trim(right(age_group, len(age_group) - 1)), '_' ,' and ') end
        as age_group
        , marital_status
        , upper(left(employment_status, 1)) + lower(right(employment_status, len(employment_status) - 1)) as employment_status
        , migration_numbers
    from dbo.unpivoted_migration_numbers
    ) A 
    join dbo.linang_common_table REG ON A.region = REG.[description] and REG.category = 'region'
    join dbo.linang_common_table EDU ON A.education_level = EDU.[description] and EDU.category = 'education'
    join dbo.linang_common_table DEST ON A.major_destination = DEST.[description] and DEST.category = 'destination'
    join dbo.linang_common_table SEX ON A.sex = SEX.[description] and SEX.category = 'sex'
    join dbo.linang_common_table AGE ON A.age_group = AGE.[description] and AGE.category = 'age'
    join dbo.linang_common_table MAR ON A.marital_status = MAR.[description] and MAR.category = 'marital'
    join dbo.linang_common_table EMP ON A.employment_status = EMP.[description] and EMP.category = 'employment'
```

---
