# EcoSphere — Database Schema

## Tables

### users
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| email | VARCHAR UNIQUE | |
| full_name | VARCHAR | |
| hashed_password | VARCHAR | bcrypt |
| role | ENUM | admin / manager / employee |
| department_id | FK → departments.id | nullable |
| xp_points | INTEGER | default 0 |
| is_active | BOOLEAN | default true |
| created_at | TIMESTAMPTZ | |

### departments
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| name | VARCHAR UNIQUE | |
| description | TEXT | |
| created_at | TIMESTAMPTZ | |

### esg_weight_settings
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| environmental_weight | FLOAT | default 40.0 |
| social_weight | FLOAT | default 30.0 |
| governance_weight | FLOAT | default 30.0 |
| updated_at | TIMESTAMPTZ | |

### app_settings
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| key | VARCHAR UNIQUE | e.g. auto_emission_calculation |
| value | VARCHAR | "true" / "false" |
| description | TEXT | |
| updated_at | TIMESTAMPTZ | |

### notifications
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| user_id | FK → users.id | |
| type | ENUM | badge_unlock / compliance_issue / … |
| title | VARCHAR | |
| message | TEXT | |
| is_read | BOOLEAN | default false |
| created_at | TIMESTAMPTZ | |

### department_scores
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| department_id | FK → departments.id | |
| environmental_score | FLOAT | |
| social_score | FLOAT | |
| governance_score | FLOAT | |
| total_score | FLOAT | |
| period | VARCHAR | e.g. "2024-Q1" |
| calculated_at | TIMESTAMPTZ | |

### emission_factors
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| name | VARCHAR | |
| source_type | ENUM | purchase / manufacturing / expense / fleet / manual |
| factor_value | FLOAT | kg CO2 per unit |
| unit | VARCHAR | kg / km / kWh |
| description | TEXT | |
| created_at | TIMESTAMPTZ | |

### carbon_transactions
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| department_id | FK → departments.id | |
| emission_factor_id | FK → emission_factors.id | nullable |
| source_type | ENUM | |
| quantity | FLOAT | |
| co2_equivalent | FLOAT | |
| description | TEXT | |
| auto_generated | BOOLEAN | |
| date | TIMESTAMPTZ | |
| created_at | TIMESTAMPTZ | |

### environmental_goals
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| title | VARCHAR | |
| description | TEXT | |
| target_value | FLOAT | |
| current_value | FLOAT | |
| unit | VARCHAR | |
| status | ENUM | active / completed / missed |
| target_date | TIMESTAMPTZ | |
| created_at | TIMESTAMPTZ | |

### csr_activities
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| title | VARCHAR | |
| description | TEXT | |
| department_id | FK → departments.id | |
| category_id | FK → categories.id | nullable |
| start_date | TIMESTAMPTZ | |
| end_date | TIMESTAMPTZ | nullable |
| max_participants | INTEGER | nullable |
| xp_reward | INTEGER | |
| created_at | TIMESTAMPTZ | |

### employee_participations
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| activity_id | FK → csr_activities.id | |
| user_id | FK → users.id | |
| status | ENUM | pending / approved / rejected |
| evidence_file | VARCHAR | file path |
| notes | TEXT | |
| submitted_at | TIMESTAMPTZ | |
| reviewed_at | TIMESTAMPTZ | nullable |

### policies
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| title | VARCHAR | |
| description | TEXT | |
| category | VARCHAR | |
| effective_date | TIMESTAMPTZ | |
| review_date | TIMESTAMPTZ | nullable |
| is_active | BOOLEAN | |
| document_url | VARCHAR | nullable |
| created_at | TIMESTAMPTZ | |

### policy_acknowledgements
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| policy_id | FK → policies.id | |
| user_id | FK → users.id | |
| acknowledged_at | TIMESTAMPTZ | |

### audits
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| title | VARCHAR | |
| department_id | FK → departments.id | |
| auditor_id | FK → users.id | |
| status | ENUM | planned / in_progress / completed / cancelled |
| score | FLOAT | nullable |
| findings | TEXT | nullable |
| scheduled_date | TIMESTAMPTZ | |
| completed_date | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | |

### compliance_issues
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| title | VARCHAR | |
| description | TEXT | |
| audit_id | FK → audits.id | nullable |
| owner_id | FK → users.id | NOT NULL |
| status | ENUM | open / in_progress / resolved / overdue |
| severity | VARCHAR | low / medium / high / critical |
| due_date | TIMESTAMPTZ | NOT NULL |
| resolved_at | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | |

### challenges
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| title | VARCHAR | |
| description | TEXT | |
| xp_reward | INTEGER | |
| status | ENUM | draft / active / under_review / completed / archived |
| start_date | TIMESTAMPTZ | nullable |
| end_date | TIMESTAMPTZ | nullable |
| created_at | TIMESTAMPTZ | |

### badges
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| name | VARCHAR UNIQUE | |
| description | TEXT | |
| icon | VARCHAR | |
| unlock_rule_type | VARCHAR | "xp" or "challenges" |
| unlock_rule_value | INTEGER | threshold |
| created_at | TIMESTAMPTZ | |

### badge_awards
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| badge_id | FK → badges.id | |
| user_id | FK → users.id | |
| awarded_at | TIMESTAMPTZ | |

### rewards
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| name | VARCHAR | |
| description | TEXT | |
| xp_cost | INTEGER | |
| stock | INTEGER | |
| is_active | BOOLEAN | |
| created_at | TIMESTAMPTZ | |

### reward_redemptions
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| reward_id | FK → rewards.id | |
| user_id | FK → users.id | |
| xp_spent | INTEGER | |
| redeemed_at | TIMESTAMPTZ | |
