from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from trainr.backend.config import config
from trainr.backend.handler.database.engine import engine
from trainr.backend.handler.model.reading import ReadingHandlerModel
from trainr.backend.handler.model.reading import ReadingZoneHandlerModel
from trainr.backend.handler.model.reading import ThresholdHandlerModel


class ReadingHandler(ABC):
    def __init__(self):
        self.threshold = None

        self.client = InfluxDBClientAsync(
            url=config.influxdb.host,
            username=config.influxdb.auth.user,
            password=config.influxdb.auth.password,
            org=config.influxdb.org
        )

    @property
    @abstractmethod
    def reading_type(self):
        pass

    @property
    @abstractmethod
    def zones_spec(self) -> List[ReadingZoneHandlerModel]:
        pass

    async def _run_influxdb_query(self, query: str) -> List[ReadingHandlerModel]:
        result = []

        query_api = self.client.query_api()
        query_results = await query_api.query(query, org=config.influxdb.org)

        for t in query_results:
            for r in t.records:
                r_value = r.get_value()
                try:
                    r_time = r['_time']
                except Exception:
                    r_time = datetime.now()

                result.append(ReadingHandlerModel(
                    reading_value=r_value, reading_type=self.reading_type, time=r_time))

        return result

    async def get_reading(self, seconds: int = 0) -> ReadingHandlerModel:
        query = f"""from(bucket: "{config.influxdb.bucket}")
                    |> range(start: -{seconds}s)
                    |> filter(fn: (r) => r._measurement == "{self.reading_type}")
                    |> last()
                    |> keep(columns: ["_time", "_value"])
        """
        try:
            results = await self._run_influxdb_query(query)

            return results[0]
        except Exception:
            return ReadingHandlerModel(reading_value=0, reading_type=self.reading_type, time=datetime.now())

    async def get_reading_avg(self, seconds: int = 10) -> ReadingHandlerModel:
        query = f"""from(bucket: "{config.influxdb.bucket}")
                            |> range(start: -{seconds}s)
                            |> filter(fn: (r) => r._measurement == "{self.reading_type}")
                            |> mean()
                """
        try:
            results = await self._run_influxdb_query(query)

            return results[0]
        except Exception:
            return ReadingHandlerModel(reading_value=0, reading_type=self.reading_type, time=datetime.now())

    async def save_reading(self, value: int):
        point = (
            Point(self.reading_type.value)
            .field('value', value)
        )

        write_api = self.client.write_api()
        await write_api.write(bucket=config.influxdb.bucket, org=config.influxdb.org, record=point)

        return ReadingHandlerModel(reading_value=value, reading_type=self.reading_type, time=datetime.now())

    def get_reading_history(self, seconds: int) -> List[ReadingHandlerModel]:
        query = f"""from(bucket: "{config.influxdb.bucket}")
                    |> range(start: -{seconds}s)
                    |> filter(fn: (r) => r._measurement == "{self.reading_type}")
                    |> keep(columns: ["_time", "_value"])
        """
        results = self._run_influxdb_query(query)

        return results

    def get_reading_zones(self) -> List[ReadingZoneHandlerModel]:
        with Session(engine) as session:
            query_statement = select(ReadingZoneHandlerModel) \
                .where(ReadingZoneHandlerModel.reading_type == self.reading_type) \
                .order_by(ReadingZoneHandlerModel.zone.asc())

            return session.scalars(query_statement).fetchall()

    def get_reading_zone(self, zone: int) -> Optional[ReadingZoneHandlerModel]:
        try:
            with Session(engine) as session:
                query_statement = select(ReadingZoneHandlerModel) \
                    .where(ReadingZoneHandlerModel.reading_type == self.reading_type) \
                    .where(ReadingZoneHandlerModel.zone == zone)

                return session.scalars(query_statement).one()
        except NoResultFound:
            return None

    def get_reading_zone_by_reading(self, reading: int) -> Optional[ReadingZoneHandlerModel]:
        zones = self.get_reading_zones()

        for z in zones:
            if z.range_from <= reading < z.range_to:
                return z

        return None

    def set_reading_zone(self, spec: ReadingZoneHandlerModel) -> ReadingZoneHandlerModel:
        if data := self.get_reading_zone(spec.zone):
            data.range_from = spec.range_from
            data.range_to = spec.range_to
            data.display_name = spec.display_name
        else:
            data = spec

        with Session(engine) as session:
            session.add(data)
            session.commit()

        return data

    def _set_zones_from_threshold(self):
        if not self.threshold:
            return None

        for z in self.zones_spec:
            try:
                f = int(int(self.threshold) * z.range_from / 100)
                n = int(int(self.threshold) * z.range_to / 100)

                self.set_reading_zone(ReadingZoneHandlerModel(
                    zone=z.zone,
                    range_from=f + 1,
                    range_to=n,
                    display_name=z.display_name,
                    reading_type=self.reading_type))
            except IndexError:
                pass

    def set_threshold(self, threshold: int):
        if data := self.get_threshold():
            data.reading_value = threshold
        else:
            data = ThresholdHandlerModel(reading_value=threshold,
                                         reading_type=self.reading_type)

        with Session(engine, expire_on_commit=True) as session:
            session.add(data)
            session.commit()

        self.threshold = threshold
        self._set_zones_from_threshold()

    def get_threshold(self) -> Optional[ThresholdHandlerModel]:
        try:
            with Session(engine) as session:
                query_statement = select(ThresholdHandlerModel) \
                    .where(ThresholdHandlerModel.reading_type == self.reading_type)

                return session.scalars(query_statement).one()
        except NoResultFound:
            return None

    def remove_history(self, seconds: int = 60 * 60):
        time_difference = datetime.now() - timedelta(seconds=seconds)

        try:
            with Session(engine) as session:
                delete_statement = delete(ReadingHandlerModel) \
                    .where(ReadingHandlerModel.time < time_difference) \
                    .where(ReadingHandlerModel.reading_type == self.reading_type)

                session.execute(delete_statement)
                session.commit()
        except:
            pass
