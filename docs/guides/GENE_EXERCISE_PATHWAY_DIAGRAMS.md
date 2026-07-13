# Gene / Exercise / Pathway 结构关系图

> 按你给的 ontology 图, `Regulated Gene` 和 `Exercise` 是直接关系,边是 `is_regulated_by`。现在 schema 已经直接增加 `exercise.csv`;这条直接边落在 `gene.exercise_id -> exercise.exercise_id`,同时保留 `gene.intervention_id -> interventions.intervention_id` 作为 protocol/provenance 连接。


---

## 图 1: 生物概念层

```mermaid
flowchart LR
    exercise["Exercise<br/>process"]
    gene["Gene<br/>paper-reported compared gene"]
    pathway["Pathway<br/>biological process / gene set"]
    phenotype["Phenotype / outcome"]

    gene -->|"is_regulated_by"| exercise
    pathway -->|"is_part_of"| gene
    pathway -->|"affects / explains"| phenotype
    exercise -->|"affects"| phenotype

    pathway -. "currently can be descriptive paper text" .-> pathway_note["library = paper_text"]
```

---

## 图 2: 当前表结构里的核心 FK

```mermaid
erDiagram
    study ||--o{ experiment : has
    study ||--o{ groups : defines
    study ||--o{ gene : reports
    study ||--o{ analysis : analyzed_as

    experiment ||--o{ interventions : has
    interventions ||--o{ exercise : represents
    experiment ||--o{ subject : has
    experiment ||--o{ sample : yields
    experiment ||--o{ assay : measured_by

    groups ||--o{ subject : assigns
    groups ||--o{ sample : assigns
    groups ||--o{ analysis : contrast_arm

    exercise ||--o{ gene : is_regulated_by

    analysis ||--o{ enrichment : produces
    pathway ||--o{ enrichment : enriched_pathway
    pathway ||--o{ gene : optional_text_link

    study {
        string study_id PK
    }
    experiment {
        string experiment_id PK
        string study_id FK
    }
    interventions {
        string intervention_id PK
        string experiment_id FK
        string material "exercise / training / running"
    }
    exercise {
        string exercise_id PK
        string study_id FK
        string experiment_id FK
        string intervention_id FK
        string exercise_name
        string exercise_type
    }
    gene {
        string gene_id PK
        string study_id FK
        string experiment_id FK
        string intervention_id FK
        string exercise_id FK
        string group_id FK
        string pathway_id FK "nullable"
        string gene_symbol
        string comparison
        string regulation_direction
        string relationship_to_exercise "is_regulated_by"
    }
    analysis {
        string analysis_id PK
        string study_id FK
        string treatment_group_id FK
        string control_group_id FK
        string contrast_label
    }
    pathway {
        string pathway_id PK
        string pathway_name
        string library "MSigDB / KEGG / paper_text"
    }
    enrichment {
        string enrichment_id PK
        string analysis_id FK
        string pathway_id FK
        string direction
        string nes
        string fdr
    }
```

---

## 图 3: gene 如何连到 exercise

```mermaid
flowchart LR
    paper["Paper text"]
    finding["reported_findings<br/>entity_type = gene"]
    gene["gene.csv"]
    exercise["exercise.csv<br/>Exercise process node"]
    intervention["interventions.csv<br/>protocol/provenance"]
    experiment["experiment.csv"]
    study["study.csv"]

    paper -->|"LLM extracts named genes + comparison + quote"| finding
    finding -->|"gene_rows_from_reported_findings"| gene

    gene -->|"is_regulated_by<br/>exercise_id"| exercise
    gene -. "protocol FK<br/>intervention_id" .-> intervention
    exercise -->|"derived from<br/>intervention_id"| intervention
    gene -->|"study_id"| study
    gene -->|"experiment_id"| experiment
    exercise -->|"experiment_id"| experiment
    intervention -->|"experiment_id"| experiment
    experiment -->|"study_id"| study

    scaffold["ensure_gene_exercise_scaffold<br/>if no intervention was extracted"]
    scaffold -. "creates minimal experiment + exercise intervention + exercise node" .-> exercise
```

查询含义:

```text
gene -> interventions -> experiment -> study
```

这条链回答的问题是:

> 这篇 exercise 文章里,哪些 gene 被比较/上调/下调/不变?

更贴近 ontology 图的说法是:

```text
gene --is_regulated_by--> exercise
```

在表里这条直接边就是:

```text
gene.exercise_id = exercise.exercise_id
gene.relationship_to_exercise = is_regulated_by
```

旧的 protocol/provenance 边仍然保留:

```text
gene.intervention_id = interventions.intervention_id
exercise.intervention_id = interventions.intervention_id
```

---

## 图 4: pathway 如何连到 exercise

```mermaid
flowchart LR
    deg["DEG / ranked gene list"]
    gsea["GSEA / enrichment"]
    enrichment["enrichment.csv<br/>pathway-exercise edge"]
    pathway["pathway.csv<br/>pathway node"]
    analysis["analysis.csv<br/>exercise contrast"]
    treated["groups.csv<br/>treatment / exercise arm"]
    control["groups.csv<br/>control / baseline arm"]
    study["study.csv"]

    deg --> gsea
    gsea --> enrichment
    enrichment -->|"pathway_id"| pathway
    enrichment -->|"analysis_id"| analysis
    analysis -->|"treatment_group_id"| treated
    analysis -->|"control_group_id"| control
    analysis -->|"study_id"| study

    pathway_note["standard pathway<br/>MSigDB / KEGG / Reactome"]
    pathway_note -. "canonical id" .-> pathway
```

查询含义:

```text
enrichment -> pathway
enrichment -> analysis -> treatment_group/control_group -> groups
```

这条链回答的问题是:

> 哪些 pathway 在 exercise vs control 的分析里显著上调/下调?

---

## 图 5: 当前状态和未来可扩展点

```mermaid
flowchart TD
    current_gene["Current gene.csv<br/>text-mined named genes"]
    exercise["Exercise<br/>exercise.csv row"]
    current_pathway["Current pathway.csv<br/>standard or descriptive pathway nodes"]
    descriptive["Descriptive pathway<br/>library = paper_text"]
    standard["Standard pathway<br/>MSigDB / KEGG / Reactome"]
    future_link["Future normalization<br/>map paper_text pathway to standard pathway id"]
    future_edge["Future reliable gene-pathway link<br/>populate gene.pathway_id or edge table"]

    current_gene -->|"is_regulated_by<br/>exercise_id"| exercise
    current_gene -. "pathway_id usually null for now" .-> current_pathway
    current_pathway --> descriptive
    current_pathway --> standard
    descriptive --> future_link
    future_link --> standard
    standard --> future_edge
    future_edge --> current_gene
```

当前推荐理解:

- `gene` 和 `exercise` 在概念上直接相连,关系是 `is_regulated_by`。
- 表实现里 `exercise` 已经是单独的 `exercise.csv` 节点,所以用 `gene.exercise_id` 直接连过去。
- `pathway` 现在先保留机制背景;标准 pathway 通过 `enrichment` 连 exercise,描述性 pathway 先不强行标准化。
- 等 pathway normalization 稳定后,再填 `gene.pathway_id` 或新增更细的 gene-pathway edge 表。
