#!/usr/bin/env python3
"""
Command-Line Interface for LAI-PrEP Bridge Period Decision Support Tool

Usage:
    python cli.py assess --input patient.json --output results.json
    python cli.py batch --input patients.csv --output-dir results/
    python cli.py validate --config lai_prep_config.json
"""

import csv
import json
import sys
from pathlib import Path

import click

# Import assessment functions
try:
    from lai_prep_decision_tool_v2_1 import (
        LAIPrEPDecisionTool,
        PatientProfile,
        assess_patient_json,
        ConfigurationError
    )
except ImportError:
    print("Error: Could not import lai_prep_decision_tool_v2_1.py")
    print("Please ensure the file is in the same directory")
    sys.exit(1)


@click.group()
@click.version_option(version='2.1.0')
def cli():
    """
    LAI-PrEP Bridge Period Decision Support Tool - Command Line Interface
    
    Assess bridge period success probability, identify barriers, and recommend
    evidence-based interventions for LAI-PrEP implementation.
    """
    pass


@cli.command()
@click.option('--input', '-i', 'input_file', required=True, 
              type=click.Path(exists=True),
              help='Input JSON file with patient data')
@click.option('--output', '-o', 'output_file', required=True, 
              type=click.Path(),
              help='Output JSON file for assessment results')
@click.option('--config', '-c', 'config_file',
              type=click.Path(exists=True),
              default=None,
              help='Configuration file (default: auto-detect)')
@click.option('--logit', is_flag=True,
              help='Use logit-space calculations (more mathematically sound)')
@click.option('--pretty', is_flag=True,
              help='Pretty-print JSON output')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def assess(input_file, output_file, config_file, logit, pretty, verbose):
    """
    Assess a single patient from JSON input
    
    Input JSON format:
    {
        "population": "PWID",
        "age": 35,
        "current_prep_status": "naive",
        "barriers": ["HOUSING_INSTABILITY", "TRANSPORTATION"],
        "healthcare_setting": "COMMUNITY_HEALTH_CENTER",
        "insurance_status": "uninsured"
    }
    """
    try:
        # Load patient data
        if verbose:
            click.echo(f"Loading patient data from: {input_file}")
        
        with open(input_file, 'r') as f:
            patient_data = json.load(f)
        
        if verbose:
            click.echo(f"Patient: {patient_data.get('population', 'Unknown')} "
                      f"age {patient_data.get('age', '?')}")
        
        # Run assessment
        if verbose:
            click.echo(f"Running assessment (method: {'logit' if logit else 'linear'})...")
        
        results = assess_patient_json(
            patient_data, 
            config_path=config_file,
            use_logit=logit
        )
        
        # Save results
        with open(output_file, 'w') as f:
            if pretty:
                json.dump(results, f, indent=2)
            else:
                json.dump(results, f)
        
        if verbose:
            click.echo(f"✓ Assessment complete")
            click.echo(f"✓ Results saved to: {output_file}")
        
        # Print summary
        click.echo("\n" + "=" * 60)
        click.echo("ASSESSMENT SUMMARY")
        click.echo("=" * 60)
        click.echo(f"Risk Level: {results['risk_assessment']['level']}")
        click.echo(f"Baseline Success: {results['risk_assessment']['baseline_success']:.1%}")
        click.echo(f"Adjusted Success: {results['risk_assessment']['adjusted_success']:.1%}")
        click.echo(f"With Interventions: {results['predictions']['with_interventions']:.1%}")
        click.echo(f"Improvement: +{results['predictions']['absolute_improvement']:.1%} "
                  f"({results['predictions']['relative_improvement_pct']:.0f}% relative)")
        
        click.echo(f"\nTop 3 Recommendations:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            click.echo(f"  {i}. {rec['intervention_name']}")
            click.echo(f"     Priority: {rec['priority']} | "
                      f"Improvement: +{rec['expected_improvement']:.1%}")
        
        click.echo("\n" + "=" * 60)
        
    except FileNotFoundError as e:
        click.echo(f"❌ Error: File not found - {e}", err=True)
        sys.exit(1)
    except json.JSONDecodeError as e:
        click.echo(f"❌ Error: Invalid JSON - {e}", err=True)
        sys.exit(1)
    except ConfigurationError as e:
        click.echo(f"❌ Configuration Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--input', '-i', 'input_file', required=True,
              type=click.Path(exists=True),
              help='Input CSV file with patient data')
@click.option('--output-dir', '-o', 'output_dir', required=True,
              type=click.Path(),
              help='Output directory for assessment results')
@click.option('--config', '-c', 'config_file',
              type=click.Path(exists=True),
              default=None,
              help='Configuration file')
@click.option('--logit', is_flag=True,
              help='Use logit-space calculations')
@click.option('--summary', is_flag=True,
              help='Generate summary CSV')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def batch(input_file, output_dir, config_file, logit, summary, verbose):
    """
    Process multiple patients from CSV input
    
    CSV format (with header):
    population,age,current_prep_status,barriers,healthcare_setting,insurance_status
    PWID,35,naive,"HOUSING_INSTABILITY,TRANSPORTATION",COMMUNITY_HEALTH_CENTER,uninsured
    MSM,28,oral_prep,"SCHEDULING_CONFLICTS",LGBTQ_CENTER,insured
    """
    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            click.echo(f"Output directory: {output_path}")
        
        # Initialize tool
        tool = LAIPrEPDecisionTool(config_path=config_file, use_logit=logit)
        
        # Read CSV
        if verbose:
            click.echo(f"Reading patients from: {input_file}")
        
        patients = []
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse barriers (comma-separated string to list)
                if 'barriers' in row and row['barriers']:
                    row['barriers'] = [b.strip() for b in row['barriers'].split(',')]
                else:
                    row['barriers'] = []
                
                # Convert age to int
                if 'age' in row:
                    row['age'] = int(row['age'])
                
                # Convert boolean fields
                for field in ['recent_hiv_test', 'transportation_access', 'childcare_needs']:
                    if field in row:
                        row[field] = row[field].lower() in ['true', '1', 'yes']
                
                patients.append(row)
        
        click.echo(f"Processing {len(patients)} patients...")
        
        # Process each patient
        results_summary = []
        
        with click.progressbar(patients, label='Assessing patients') as bar:
            for i, patient_data in enumerate(bar):
                try:
                    # Create profile and assess
                    profile = PatientProfile.from_dict(patient_data)
                    assessment = tool.assess_patient(profile)
                    
                    # Generate output filename
                    patient_id = patient_data.get('patient_id', f'patient_{i+1:04d}')
                    output_file = output_path / f"{patient_id}_assessment.json"
                    
                    # Save individual assessment
                    json_output = assessment.to_json(profile)
                    with open(output_file, 'w') as f:
                        json.dump(json_output, f, indent=2)
                    
                    # Collect summary data
                    results_summary.append({
                        'patient_id': patient_id,
                        'population': patient_data['population'],
                        'age': patient_data['age'],
                        'prep_status': patient_data['current_prep_status'],
                        'barrier_count': len(patient_data['barriers']),
                        'risk_level': assessment.attrition_risk,
                        'baseline_success': assessment.baseline_success_rate,
                        'adjusted_success': assessment.adjusted_success_rate,
                        'estimated_success': assessment.estimated_success_with_interventions,
                        'improvement': assessment.estimated_success_with_interventions - 
                                      assessment.adjusted_success_rate,
                        'top_intervention': assessment.recommended_interventions[0].intervention_name
                                          if assessment.recommended_interventions else 'None'
                    })
                    
                except Exception as e:
                    click.echo(f"\n⚠️  Error processing patient {i+1}: {e}", err=True)
                    continue
        
        click.echo(f"\n✓ Processed {len(results_summary)} patients successfully")
        click.echo(f"✓ Individual assessments saved to: {output_path}")
        
        # Generate summary CSV if requested
        if summary and results_summary:
            summary_file = output_path / "batch_summary.csv"
            
            with open(summary_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results_summary[0].keys())
                writer.writeheader()
                writer.writerows(results_summary)
            
            click.echo(f"✓ Summary saved to: {summary_file}")
            
            # Print aggregate statistics
            click.echo("\n" + "=" * 60)
            click.echo("BATCH SUMMARY STATISTICS")
            click.echo("=" * 60)
            
            total = len(results_summary)
            avg_baseline = sum(r['baseline_success'] for r in results_summary) / total
            avg_adjusted = sum(r['adjusted_success'] for r in results_summary) / total
            avg_estimated = sum(r['estimated_success'] for r in results_summary) / total
            avg_improvement = sum(r['improvement'] for r in results_summary) / total
            
            click.echo(f"Total Patients: {total}")
            click.echo(f"Average Baseline Success: {avg_baseline:.1%}")
            click.echo(f"Average Adjusted Success: {avg_adjusted:.1%}")
            click.echo(f"Average With Interventions: {avg_estimated:.1%}")
            click.echo(f"Average Improvement: +{avg_improvement:.1%}")
            
            # Risk distribution
            from collections import Counter
            risk_counts = Counter(r['risk_level'] for r in results_summary)
            click.echo("\nRisk Level Distribution:")
            for level, count in risk_counts.most_common():
                click.echo(f"  {level}: {count} ({count/total:.0%})")
            
            click.echo("=" * 60)
        
    except FileNotFoundError as e:
        click.echo(f"❌ Error: File not found - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', 'config_file', required=True,
              type=click.Path(exists=True),
              help='Configuration file to validate')
@click.option('--verbose', '-v', is_flag=True,
              help='Verbose output')
def validate(config_file, verbose):
    """
    Validate configuration file
    """
    try:
        click.echo(f"Validating configuration: {config_file}")
        
        # Try to load configuration
        from lai_prep_decision_tool_v2_1 import Configuration
        config = Configuration(config_file)
        
        click.echo("✓ JSON syntax valid")
        click.echo(f"✓ Version: {config.config.get('version', 'Unknown')}")
        
        # Check sections
        sections = [
            'populations', 'barriers', 'interventions',
            'healthcare_settings', 'risk_categories', 'algorithm_parameters'
        ]
        
        for section in sections:
            count = len(config.config.get(section, {}))
            click.echo(f"✓ Section '{section}': {count} entries")
        
        if verbose:
            click.echo("\nPopulations:")
            for key, data in config.config['populations'].items():
                click.echo(f"  • {key}: {data['name']} "
                          f"(baseline attrition: {data['baseline_attrition']:.0%})")
            
            click.echo("\nInterventions:")
            for key, data in config.config['interventions'].items():
                click.echo(f"  • {key}: {data['name']} "
                          f"(improvement: +{data['improvement']*100:.1f}%)")
        
        click.echo("\n" + "=" * 60)
        click.echo("✅ CONFIGURATION VALID")
        click.echo("=" * 60)
        
    except ConfigurationError as e:
        click.echo(f"❌ Configuration Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option('--output', '-o', 'output_file',
              type=click.Path(),
              default='patient_template.json',
              help='Output template file')
def template(output_file):
    """
    Generate a patient data template
    """
    template_data = {
        "patient_id": "patient_001",
        "population": "MSM",
        "age": 30,
        "current_prep_status": "naive",
        "barriers": [
            "SCHEDULING_CONFLICTS"
        ],
        "healthcare_setting": "COMMUNITY_HEALTH_CENTER",
        "insurance_status": "insured",
        "recent_hiv_test": False,
        "transportation_access": True,
        "childcare_needs": False,
        "_comment": "Valid populations: MSM, CISGENDER_WOMEN, TRANSGENDER_WOMEN, ADOLESCENT, PWID, PREGNANT_LACTATING, GENERAL",
        "_comment2": "Valid prep_status: naive, oral_prep, discontinued_oral",
        "_comment3": "See documentation for complete list of barriers and settings"
    }
    
    with open(output_file, 'w') as f:
        json.dump(template_data, f, indent=2)
    
    click.echo(f"✓ Template saved to: {output_file}")
    click.echo("\nEdit this file with your patient data, then run:")
    click.echo(f"  python cli.py assess -i {output_file} -o results.json")


if __name__ == '__main__':
    cli()
