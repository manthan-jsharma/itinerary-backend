"""Initial migration

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2023-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa



revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('locations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('region', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_locations_id'), 'locations', ['id'], unique=False)
    

    op.create_table('accommodations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price_per_night', sa.Float(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('amenities', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accommodations_id'), 'accommodations', ['id'], unique=False)
    

    op.create_table('transfers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('from_location_id', sa.Integer(), nullable=False),
        sa.Column('to_location_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['from_location_id'], ['locations.id'], ),
        sa.ForeignKeyConstraint(['to_location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transfers_id'), 'transfers', ['id'], unique=False)
    

    op.create_table('activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('location_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activities_id'), 'activities', ['id'], unique=False)
    

    op.create_table('itineraries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('num_nights', sa.Integer(), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('is_recommended', sa.Boolean(), nullable=True),
        sa.Column('regions', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_itineraries_id'), 'itineraries', ['id'], unique=False)
    

    op.create_table('itinerary_accommodation',
        sa.Column('itinerary_id', sa.Integer(), nullable=False),
        sa.Column('accommodation_id', sa.Integer(), nullable=False),
        sa.Column('day_number', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['accommodation_id'], ['accommodations.id'], ),
        sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], ),
        sa.PrimaryKeyConstraint('itinerary_id', 'accommodation_id')
    )
    
    op.create_table('itinerary_activity',
        sa.Column('itinerary_id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.Column('day_number', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
        sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], ),
        sa.PrimaryKeyConstraint('itinerary_id', 'activity_id')
    )
    
    op.create_table('itinerary_transfer',
        sa.Column('itinerary_id', sa.Integer(), nullable=False),
        sa.Column('transfer_id', sa.Integer(), nullable=False),
        sa.Column('day_number', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], ),
        sa.ForeignKeyConstraint(['transfer_id'], ['transfers.id'], ),
        sa.PrimaryKeyConstraint('itinerary_id', 'transfer_id')
    )


def downgrade() -> None:
    # Drop association tables
    op.drop_table('itinerary_transfer')
    op.drop_table('itinerary_activity')
    op.drop_table('itinerary_accommodation')
    
    # Drop main tables
    op.drop_index(op.f('ix_itineraries_id'), table_name='itineraries')
    op.drop_table('itineraries')
    
    op.drop_index(op.f('ix_activities_id'), table_name='activities')
    op.drop_table('activities')
    
    op.drop_index(op.f('ix_transfers_id'), table_name='transfers')
    op.drop_table('transfers')
    
    op.drop_index(op.f('ix_accommodations_id'), table_name='accommodations')
    op.drop_table('accommodations')
    
    op.drop_index(op.f('ix_locations_id'), table_name='locations')
    op.drop_table('locations')