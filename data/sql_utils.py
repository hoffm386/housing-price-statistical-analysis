import psycopg2

def create_database():
    """
    This function assumes that you have an existing database called `postgres`
    without any username/password required to access it.  Then it creates a new
    database called `housing_data`
    """
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True # it seems this mode is needed to make a db
    conn.set_isolation_level(0) # also this for dropping db
    cursor = conn.cursor()
    DROP_OLD_DATABASE_QUERY = "DROP DATABASE housing_data;"
    cursor.execute(DROP_OLD_DATABASE_QUERY)
    CREATE_DATABASE_QUERY = "CREATE DATABASE housing_data;"
    cursor.execute(CREATE_DATABASE_QUERY)
    conn.close()

def create_sales_table(conn):
    CREATE_SALES_TABLE_QUERY = """
        DROP TABLE IF EXISTS sales;
        CREATE TABLE sales (
            ExciseTaxNbr       INT,
            Major              CHAR(6),
            Minor              CHAR(4),
            DocumentDate       DATE,
            SalePrice          INT,
            RecordingNbr       CHAR(14),
            Volume             CHAR(3),
            Page               CHAR(3),
            PlatNbr            CHAR(6),
            PlatType           CHAR(1),
            PlatLot            CHAR(14),
            PlatBlock          CHAR(7),
            SellerName         TEXT,
            BuyerName          TEXT,
            PropertyType       INT,
            PrincipalUse       INT,
            SaleInstrument     INT,
            AFForestLand       CHAR(1),
            AFCurrentUseLand   CHAR(1),
            AFNonProfitUse     CHAR(1),
            AFHistoricProperty CHAR(1),
            SaleReason         INT,
            PropertyClass      INT,
            SaleWarning        TEXT
        );
    """
    cursor = conn.cursor()
    cursor.execute(CREATE_SALES_TABLE_QUERY)
    conn.commit()

def create_buildings_table(conn):
    CREATE_BUILDINGS_TABLE_QUERY = """
        DROP TABLE IF EXISTS buildings;
        CREATE TABLE buildings (
            Major              CHAR(6),
            Minor              CHAR(4),
            BldgNbr            INT,
            NbrLivingUnits     INT,
            Address            TEXT,
            BuildingNumber     CHAR(5),
            Fraction           CHAR(3),
            DirectionPrefix    CHAR(2),
            StreetName         CHAR(25),
            StreetType         CHAR(6),
            DirectionSuffix    CHAR(2),
            ZipCode            CHAR(10),
            Stories            REAL,
            BldgGrade          INT,
            BldgGradeVar       INT,
            SqFt1stFloor       INT,
            SqFtHalfFloor      INT,
            SqFt2ndFloor       INT,
            SqFtUpperFloor     INT,
            SqFtUnfinFull      INT,
            SqFtUnfinHalf      INT,
            SqFtTotLiving      INT,
            SqFtTotBasement    INT,
            SqFtFinBasement    INT,
            FinBasementGrade   INT,
            SqFtGarageBasement INT,
            SqFtGarageAttached INT,
            DaylightBasement   CHAR(1),
            SqFtOpenPorch      INT,
            SqFtEnclosedPorch  INT,
            SqFtDeck           INT,
            HeatSystem         INT,
            HeatSource         INT,
            BrickStone         INT,
            ViewUtilization    CHAR(1),
            Bedrooms           INT,
            BathHalfCount      INT,
            Bath3qtrCount      INT,
            BathFullCount      INT,
            FpSingleStory      INT,
            FpMultiStory       INT,
            FpFreestanding     INT,
            FpAdditional       INT,
            YrBuilt            INT,
            YrRenovated        INT,
            PcntComplete       INT,
            Obsolescence       INT,
            PcntNetCondition   INT,
            Condition          INT,
            AddnlCost          INT
        );
    """
    cursor = conn.cursor()
    cursor.execute(CREATE_BUILDINGS_TABLE_QUERY)
    conn.commit()

def create_parcels_table(conn):
    CREATE_PARCELS_TABLE_QUERY = """
        DROP TABLE IF EXISTS parcels;
        CREATE TABLE parcels (
            Major                  CHAR(6),
            Minor                  CHAR(4),
            PropName               CHAR(80),
            PlatName               CHAR(50),
            PlatLot                CHAR(14),
            PlatBlock              CHAR(7),
            Range                  INT,
            Township               INT,
            Section                INT,
            QuarterSection         CHAR(2),
            PropType               CHAR(1),
            Area                   CHAR(3),
            SubArea                CHAR(3),
            SpecArea               CHAR(3),
            SpecSubArea            CHAR(3),
            DistrictName           CHAR(80),
            LevyCode               CHAR(4),
            CurrentZoning          CHAR(50),
            HBUAsIfVacant          INT,
            HBUAsImproved          INT,
            PresentUse             INT,
            SqFtLot                INT,
            WaterSystem            INT,
            SewerSystem            INT,
            Access                 INT,
            Topography             INT,
            StreetSurface          INT,
            RestrictiveSzShape     INT,
            InadequateParking      INT,
            PcntUnusable           INT,
            Unbuildable            CHAR(5), -- "Unbuildable" is not in the DOC
            MtRainier              INT,
            Olympics               INT,
            Cascades               INT,
            Territorial            INT,
            SeattleSkyline         INT,
            PugetSound             INT,
            LakeWashington         INT,
            LakeSammamish          INT,
            SmallLakeRiverCreek    INT,
            OtherView              INT,
            WfntLocation           INT,
            WfntFootage            INT,
            WfntBank               INT,
            WfntPoorQuality        INT,
            WfntRestrictedAccess   INT,
            WfntAccessRights       CHAR(1),
            WfntProximityInfluence CHAR(1),
            TidelandShoreland      INT,
            LotDepthFactor         INT,
            TrafficNoise           INT,
            AirportNoise           INT,
            PowerLines             CHAR(1),
            OtherNuisances         CHAR(1),
            NbrBldgSites           INT,
            Contamination          INT,
            DNRLease               CHAR(1),
            AdjacentGolfFairway    CHAR(1),
            AdjacentGreenbelt      CHAR(1),
            -- "Common Property" is listed here in the DOC, but isn't in the CSV
            HistoricSite           INT,
            CurrentUseDesignation  INT,
            NativeGrowthProtEsmt   CHAR(1),
            Easements              CHAR(1),
            OtherDesignation       CHAR(1),
            DeedRestrictions       CHAR(1),
            DevelopmentRightsPurch CHAR(1),
            CoalMineHazard         CHAR(1),
            CriticalDrainage       CHAR(1),
            ErosionHazard          CHAR(1),
            LandfillBuffer         CHAR(1),
            HundredYrFloodPlain    CHAR(1),
            SeismicHazard          CHAR(1),
            LandslideHazard        CHAR(1),
            SteepSlopeHazard       CHAR(1),
            Stream                 CHAR(1),
            Wetland                CHAR(1),
            SpeciesOfConcern       CHAR(1),
            SensitiveAreaTract     CHAR(1),
            WaterProblems          CHAR(1),
            TranspConcurrency      CHAR(1),
            OtherProblems          CHAR(1)
        );
    """
    cursor = conn.cursor()
    cursor.execute(CREATE_PARCELS_TABLE_QUERY)
    conn.commit()

def copy_csv_to_sales_table(conn, sales_csv_file):
    # skip the header row
    next(sales_csv_file)

    COPY_SALES_QUERY = """COPY sales FROM STDIN WITH (FORMAT CSV)"""
    cursor = conn.cursor()
    cursor.copy_expert(COPY_SALES_QUERY, sales_csv_file)
    conn.commit()

def copy_csv_to_buildings_table(conn, buildings_csv_file):
    # skip the header row
    next(buildings_csv_file)

    COPY_BUILDINGS_QUERY = """COPY buildings FROM STDIN WITH (FORMAT CSV)"""
    cursor = conn.cursor()
    cursor.copy_expert(COPY_BUILDINGS_QUERY, buildings_csv_file)
    conn.commit()

def copy_csv_to_parcels_table(conn, parcels_csv_file):
    # skip the header row
    next(parcels_csv_file)

    COPY_PARCELS_QUERY = """COPY parcels FROM STDIN WITH (FORMAT CSV)"""
    cursor = conn.cursor()
    cursor.copy_expert(COPY_PARCELS_QUERY, parcels_csv_file)
    conn.commit()
