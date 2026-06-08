import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import json
from typing import Dict, List, Tuple

class RealWorldDataGenerator:
    """
    Generate realistic financial datasets based on real-world economic scenarios
    and critical financial issues that users face in developing economies
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        
        # Real-world economic parameters (India-specific)
        self.inflation_rates = {
            'food': 6.5, 'housing': 8.2, 'transport': 9.1, 
            'education': 11.3, 'healthcare': 12.7, 'overall': 7.8
        }
        self.unemployment_rate = 7.8
        self.gdp_growth = 6.3
        self.interest_rates = {'savings': 4.0, 'personal_loan': 11.5, 'home_loan': 8.5}
        
        # Critical financial scenarios
        self.critical_scenarios = [
            'job_loss', 'medical_emergency', 'market_crash', 
            'inflation_spike', 'debt_crisis', 'business_failure'
        ]

    def generate_financial_crisis_dataset(self, n_samples: int = 50000) -> pd.DataFrame:
        """
        Generate dataset simulating various financial crises and their impacts
        """
        data = []
        
        for i in range(n_samples):
            # User demographics
            age = np.random.normal(35, 12)
            age = max(22, min(65, age))
            income_level = self._get_income_bracket(age)
            
            # Crisis scenario
            scenario = random.choice(self.critical_scenarios)
            crisis_severity = np.random.beta(2, 5)  # Most crises are moderate
            
            # Financial metrics before crisis
            monthly_income = self._generate_income(income_level, age)
            monthly_expenses = self._generate_expenses(monthly_income, scenario)
            emergency_fund = np.random.uniform(0, 12) * monthly_income  # 0-12 months
            total_debt = np.random.uniform(0, 5) * monthly_income
            
            # Crisis impact calculation
            income_loss = self._calculate_income_loss(scenario, crisis_severity, age)
            expense_increase = self._calculate_expense_increase(scenario, crisis_severity)
            
            # Post-crisis financial state
            post_crisis_income = monthly_income * (1 - income_loss)
            post_crisis_expenses = monthly_expenses * (1 + expense_increase)
            
            # Survival calculation
            monthly_survival_days = (emergency_fund / post_crisis_expenses) * 30
            survival_months = emergency_fund / post_crisis_expenses
            
            # Risk factors
            debt_to_income = total_debt / monthly_income
            savings_rate = (monthly_income - monthly_expenses) / monthly_income
            financial_stress = self._calculate_financial_stress(
                post_crisis_income, post_crisis_expenses, total_debt
            )
            
            # Recovery potential
            recovery_months = self._estimate_recovery_time(scenario, crisis_severity, age, skills_level=np.random.uniform(0.3, 1.0))
            
            data.append({
                'user_id': f"USER_{i:06d}",
                'age': age,
                'income_bracket': income_level,
                'monthly_income': monthly_income,
                'monthly_expenses': monthly_expenses,
                'emergency_fund_months': emergency_fund / monthly_income,
                'total_debt': total_debt,
                'debt_to_income_ratio': debt_to_income,
                'savings_rate': savings_rate,
                'crisis_scenario': scenario,
                'crisis_severity': crisis_severity,
                'income_loss_percentage': income_loss,
                'expense_increase_percentage': expense_increase,
                'post_crisis_income': post_crisis_income,
                'post_crisis_expenses': post_crisis_expenses,
                'survival_months': survival_months,
                'financial_stress_score': financial_stress,
                'recovery_months': recovery_months,
                'will_default': 1 if survival_months < 3 and debt_to_income > 0.5 else 0,
                'needs_intervention': 1 if financial_stress > 0.8 else 0,
                'timestamp': datetime.now() - timedelta(days=random.randint(0, 730))
            })
        
        return pd.DataFrame(data)

    def generate_fraud_detection_dataset(self, n_samples: int = 100000) -> pd.DataFrame:
        """
        Enhanced fraud detection dataset with real-world patterns
        """
        data = []
        
        for i in range(n_samples):
            # Transaction characteristics
            amount = np.random.lognormal(2.7, 0.7)
            merchant_category = random.choice([
                'retail', 'dining', 'travel', 'utilities', 'online', 
                'gambling', 'crypto', 'remittance', 'education', 'healthcare'
            ])
            
            # User behavior patterns
            user_id = random.randint(1, 10000)
            account_age = np.random.uniform(1, 3650)
            typical_transaction_amount = np.random.lognormal(2.7, 0.6)
            
            # Fraud indicators
            is_fraud = random.random() < 0.04  # 4% fraud rate
            geographic_distance = np.random.uniform(0, 1200)
            time_since_last_tx = np.random.exponential(30)
            device_mismatch = random.random() < 0.08
            velocity_check = np.random.uniform(0, 8)
            
            if is_fraud:
                # Fraud patterns
                amount *= np.random.uniform(6, 18)  # Clearly higher amounts
                geographic_distance = np.random.uniform(1500, 10000)  # Unusual locations
                time_since_last_tx = np.random.uniform(0.01, 0.75)  # Rapid transactions
                device_mismatch = random.random() < 0.95  # Much more likely device mismatch
                velocity_check = np.random.uniform(12, 60)  # High velocity
                
                # Specific fraud scenarios
                fraud_type = random.choice(['account_takeover', 'card_theft', 'identity_theft', 'synthetic_identity'])
                if fraud_type == 'account_takeover':
                    merchant_category = random.choice(['online', 'crypto', 'gambling'])
                elif fraud_type == 'card_theft':
                    geographic_distance = np.random.uniform(1000, 10000)
            else:
                # Non-fraud transactions stay in a much tighter behavioral band.
                amount = np.clip(amount, 2, 400)
                geographic_distance = np.random.uniform(0, 900)
                time_since_last_tx = np.random.exponential(36)
                velocity_check = np.random.uniform(0, 6)
            
            # Risk scoring features
            ip_risk_score = self._calculate_ip_risk(geographic_distance, device_mismatch)
            transaction_risk = self._calculate_transaction_risk(
                amount, typical_transaction_amount, time_since_last_tx, velocity_check
            )
            
            data.append({
                'transaction_id': f"TX_{i:06d}",
                'user_id': user_id,
                'amount': amount,
                'merchant_category': merchant_category,
                'timestamp': datetime.now() - timedelta(minutes=random.randint(0, 43200)),
                'geographic_distance': geographic_distance,
                'time_since_last_tx': time_since_last_tx,
                'device_mismatch': int(device_mismatch),
                'velocity_check': velocity_check,
                'ip_risk_score': ip_risk_score,
                'transaction_risk_score': transaction_risk,
                'account_age_days': account_age,
                'typical_transaction_amount': typical_transaction_amount,
                'amount_deviation': amount / typical_transaction_amount,
                'is_fraud': int(is_fraud),
                'fraud_type': 'account_takeover' if is_fraud and random.random() < 0.3 else 'other'
            })
        
        return pd.DataFrame(data)

    def generate_income_volatility_dataset(self, n_samples: int = 30000) -> pd.DataFrame:
        """
        Dataset for income prediction and volatility analysis
        """
        data = []
        
        for i in range(n_samples):
            # Professional profile
            age = np.random.normal(38, 10)
            age = max(22, min(60, age))
            education = random.choice(['high_school', 'bachelors', 'masters', 'phd'])
            industry = random.choice([
                'technology', 'healthcare', 'finance', 'manufacturing', 
                'retail', 'education', 'government', 'gig_economy'
            ])
            experience_years = max(0, age - 22 - random.randint(0, 8))
            
            # Income profile
            base_salary = self._calculate_base_salary(education, industry, experience_years)
            variable_income = np.random.uniform(0, 0.4) * base_salary  # Bonuses/commissions
            
            # Economic factors
            gdp_growth_impact = np.random.normal(self.gdp_growth/100, 0.02)
            industry_growth = self._get_industry_growth(industry)
            skill_relevance = np.random.uniform(0.3, 1.0)
            
            # Risk factors
            job_stability_score = self._calculate_job_stability(industry, experience_years, skill_relevance)
            automation_risk = self._calculate_automation_risk(industry, skill_relevance)
            
            # Monthly income simulation (12 months)
            monthly_incomes = []
            for month in range(12):
                seasonal_factor = 1.0
                if industry in 'retail':
                    seasonal_factor = 1.2 if month in [10, 11] else 0.9
                elif industry == 'education':
                    seasonal_factor = 1.1 if month in [7, 8] else 0.95
                
                random_factor = np.random.normal(1.0, 0.15)
                monthly_income = (base_salary + variable_income * random_factor) * seasonal_factor * (1 + gdp_growth_impact)
                monthly_incomes.append(max(0, monthly_income))
            
            # Calculate volatility metrics
            income_std = np.std(monthly_incomes)
            income_cv = income_std / np.mean(monthly_incomes)
            worst_month_income = min(monthly_incomes)
            best_month_income = max(monthly_incomes)
            
            # Predictive features
            income_trend = (monthly_incomes[-1] - monthly_incomes[0]) / monthly_incomes[0] if monthly_incomes[0] > 0 else 0
            savings_potential = (np.mean(monthly_incomes) * 0.2)  # 20% savings potential
            
            data.append({
                'user_id': f"USER_{i:06d}",
                'age': age,
                'education': education,
                'industry': industry,
                'experience_years': experience_years,
                'base_salary': base_salary,
                'variable_income_ratio': variable_income / base_salary,
                'job_stability_score': job_stability_score,
                'automation_risk_score': automation_risk,
                'industry_growth_rate': industry_growth,
                'skill_relevance_score': skill_relevance,
                'monthly_income_mean': np.mean(monthly_incomes),
                'monthly_income_std': income_std,
                'income_coefficient_of_variation': income_cv,
                'worst_month_income': worst_month_income,
                'best_month_income': best_month_income,
                'income_trend_12m': income_trend,
                'savings_potential_monthly': savings_potential,
                'layoff_risk_score': 1 - job_stability_score,
                'income_volatility_risk': 'high' if income_cv > 0.3 else 'medium' if income_cv > 0.15 else 'low'
            })
        
        return pd.DataFrame(data)

    def _get_income_bracket(self, age: int) -> str:
        """Get income bracket based on age and experience"""
        if age < 30:
            return random.choice(['entry_level', 'junior'])
        elif age < 45:
            return random.choice(['mid_level', 'senior'])
        else:
            return random.choice(['senior', 'executive'])

    def _generate_income(self, bracket: str, age: int) -> float:
        """Generate realistic income based on bracket and age"""
        base_incomes = {
            'entry_level': 25000,
            'junior': 35000,
            'mid_level': 60000,
            'senior': 120000,
            'executive': 250000
        }
        base = base_incomes[bracket]
        return np.random.normal(base, base * 0.2)

    def _generate_expenses(self, income: float, scenario: str) -> float:
        """Generate expenses based on income and scenario"""
        base_ratio = 0.7  # 70% of income typically
        
        scenario_multipliers = {
            'medical_emergency': 1.5,
            'inflation_spike': 1.3,
            'job_loss': 0.8,  # Reduced expenses due to cost-cutting
            'market_crash': 0.9,
            'debt_crisis': 1.2,
            'business_failure': 0.85
        }
        
        multiplier = scenario_multipliers.get(scenario, 1.0)
        return income * base_ratio * multiplier * np.random.uniform(0.8, 1.2)

    def _calculate_income_loss(self, scenario: str, severity: float, age: int) -> float:
        """Calculate income loss percentage based on scenario"""
        base_losses = {
            'job_loss': 1.0,
            'business_failure': 0.8,
            'market_crash': 0.3,
            'medical_emergency': 0.2,
            'inflation_spike': 0.1,
            'debt_crisis': 0.15
        }
        
        base_loss = base_losses.get(scenario, 0.2)
        age_factor = 1.0 if age < 45 else 1.2  # Older workers face harder reemployment
        
        return min(1.0, base_loss * severity * age_factor)

    def _calculate_expense_increase(self, scenario: str, severity: float) -> float:
        """Calculate expense increase percentage"""
        base_increases = {
            'medical_emergency': 2.0,
            'inflation_spike': 1.5,
            'debt_crisis': 0.8,
            'job_loss': -0.3,  # Expense reduction
            'market_crash': 0.2,
            'business_failure': 0.1
        }
        
        return base_increases.get(scenario, 0.1) * severity

    def _calculate_financial_stress(self, income: float, expenses: float, debt: float) -> float:
        """Calculate financial stress score (0-1)"""
        if income <= 0:
            return 1.0
        
        expense_ratio = expenses / income
        debt_service_ratio = (debt * 0.1) / income  # 10% annual debt service
        
        stress = min(1.0, (expense_ratio + debt_service_ratio) / 2)
        return stress

    def _estimate_recovery_time(self, scenario: str, severity: float, age: int, skills_level: float) -> int:
        """Estimate recovery time in months"""
        base_recovery = {
            'job_loss': 6,
            'medical_emergency': 3,
            'market_crash': 12,
            'inflation_spike': 24,
            'debt_crisis': 18,
            'business_failure': 24
        }
        
        base = base_recovery.get(scenario, 12)
        age_factor = 1.0 if age < 40 else 1.5
        skills_factor = 2.0 - skills_level  # Better skills = faster recovery
        
        return int(base * severity * age_factor * skills_factor)

    def _calculate_ip_risk(self, geo_distance: float, device_mismatch: bool) -> float:
        """Calculate IP-based risk score"""
        geo_risk = min(1.0, geo_distance / 5000)
        device_risk = 0.7 if device_mismatch else 0.1
        return (geo_risk + device_risk) / 2

    def _calculate_transaction_risk(self, amount: float, typical: float, time_gap: float, velocity: float) -> float:
        """Calculate transaction-level risk score"""
        amount_risk = min(1.0, (amount / typical - 1) if amount > typical else 0)
        time_risk = max(0, 1 - time_gap / 24)  # Recent transactions
        velocity_risk = min(1.0, velocity / 20)
        
        return (amount_risk + time_risk + velocity_risk) / 3

    def _calculate_base_salary(self, education: str, industry: str, experience: float) -> float:
        """Calculate base salary based on qualifications"""
        education_multipliers = {
            'high_school': 1.0,
            'bachelors': 1.8,
            'masters': 2.5,
            'phd': 3.2
        }
        
        industry_multipliers = {
            'technology': 1.5,
            'finance': 1.4,
            'healthcare': 1.2,
            'manufacturing': 1.0,
            'retail': 0.8,
            'education': 0.9,
            'government': 1.1,
            'gig_economy': 0.7
        }
        
        base = 30000  # Base salary
        edu_mult = education_multipliers[education]
        ind_mult = industry_multipliers[industry]
        exp_mult = 1 + (experience / 20)  # 5% increase per year of experience
        
        return base * edu_mult * ind_mult * exp_mult

    def _calculate_job_stability(self, industry: str, experience: float, skills: float) -> float:
        """Calculate job stability score (0-1)"""
        industry_stability = {
            'government': 0.95,
            'healthcare': 0.85,
            'education': 0.80,
            'manufacturing': 0.75,
            'finance': 0.70,
            'technology': 0.65,
            'retail': 0.60,
            'gig_economy': 0.30
        }
        
        base_stability = industry_stability[industry]
        experience_bonus = min(0.2, experience / 50)
        skills_bonus = skills * 0.3
        
        return min(1.0, base_stability + experience_bonus + skills_bonus)

    def _calculate_automation_risk(self, industry: str, skills: float) -> float:
        """Calculate automation risk score (0-1)"""
        industry_risk = {
            'manufacturing': 0.8,
            'retail': 0.7,
            'finance': 0.6,
            'technology': 0.4,
            'healthcare': 0.3,
            'education': 0.2,
            'government': 0.1,
            'gig_economy': 0.5
        }
        
        return industry_risk[industry] * (1 - skills)

    def _get_industry_growth(self, industry: str) -> float:
        """Get industry growth rate"""
        growth_rates = {
            'technology': 0.12,
            'healthcare': 0.08,
            'finance': 0.06,
            'manufacturing': 0.04,
            'retail': 0.03,
            'education': 0.05,
            'government': 0.02,
            'gig_economy': 0.15
        }
        
        return growth_rates.get(industry, 0.05)

    def save_datasets(
        self,
        output_dir: str = "data/real_world",
        crisis_samples: int = 50000,
        fraud_samples: int = 100000,
        income_samples: int = 30000,
    ):
        """Generate and save all datasets"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating financial crisis dataset...")
        crisis_data = self.generate_financial_crisis_dataset(crisis_samples)
        crisis_data.to_csv(f"{output_dir}/financial_crisis_dataset.csv", index=False)
        
        print("Generating enhanced fraud detection dataset...")
        fraud_data = self.generate_fraud_detection_dataset(fraud_samples)
        fraud_data.to_csv(f"{output_dir}/fraud_detection_enhanced.csv", index=False)
        
        print("Generating income volatility dataset...")
        income_data = self.generate_income_volatility_dataset(income_samples)
        income_data.to_csv(f"{output_dir}/income_volatility_dataset.csv", index=False)
        
        # Generate summary statistics
        summary = {
            'datasets': {
                'financial_crisis': {
                    'samples': len(crisis_data),
                    'features': len(crisis_data.columns),
                    'crisis_types': crisis_data['crisis_scenario'].unique().tolist(),
                    'avg_survival_months': crisis_data['survival_months'].mean(),
                    'default_rate': crisis_data['will_default'].mean()
                },
                'fraud_detection': {
                    'samples': len(fraud_data),
                    'features': len(fraud_data.columns),
                    'fraud_rate': fraud_data['is_fraud'].mean(),
                    'avg_transaction_amount': fraud_data['amount'].mean()
                },
                'income_volatility': {
                    'samples': len(income_data),
                    'features': len(income_data.columns),
                    'avg_income_volatility': income_data['income_coefficient_of_variation'].mean(),
                    'high_layoff_risk_percentage': (income_data['layoff_risk_score'] > 0.7).mean()
                }
            },
            'generation_timestamp': datetime.now().isoformat()
        }
        
        with open(f"{output_dir}/dataset_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Datasets saved to {output_dir}")
        print(f"Summary: {summary}")

if __name__ == "__main__":
    generator = RealWorldDataGenerator()
    generator.save_datasets()
