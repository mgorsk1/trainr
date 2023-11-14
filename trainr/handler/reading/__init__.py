from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from trainr.handler.database.engine import engine
from trainr.handler.model.reading import ReadingZoneHandlerModel, ReadingHandlerModel, ThresholdHandlerModel


class ReadingHandler(ABC):
    def __init__(self):
        self.threshold = None

    @property
    @abstractmethod
    def reading_type(self):
        pass

    def get_reading(self, seconds: int = 0) -> ReadingHandlerModel:
        with Session(engine) as session:
            query_statement = select(ReadingHandlerModel) \
                .where(ReadingHandlerModel.reading_type == self.reading_type) \
                .order_by(ReadingHandlerModel.time.desc()) \
                .limit(1)

            if seconds > 0:
                time_difference = datetime.now() - timedelta(seconds=seconds)
                query_statement = query_statement.where(ReadingHandlerModel.time >= time_difference)

            try:
                return session.scalars(query_statement).one()
            except NoResultFound:
                data = ReadingHandlerModel(
                    reading_value=0, reading_type=self.reading_type, time=datetime.now())

                return data

    def save_reading(self, value: int):
        with Session(engine, expire_on_commit=False) as session:
            data = ReadingHandlerModel(reading_value=value,
                                       reading_type=self.reading_type,
                                       time=datetime.now())

            session.add(data)
            session.commit()

        return data

    def get_reading_history(self, seconds: int) -> List[ReadingHandlerModel]:
        time_difference = datetime.now() - timedelta(seconds=seconds)

        with Session(engine) as session:
            query_statement = select(ReadingHandlerModel) \
                .where(ReadingHandlerModel.reading_type == self.reading_type) \
                .where(ReadingHandlerModel.time >= time_difference)

            return session.scalars(query_statement).fetchall()

    def get_reading_zones(self) -> List[ReadingZoneHandlerModel]:
        with Session(engine) as session:
            query_statement = select(ReadingZoneHandlerModel) \
                .where(ReadingZoneHandlerModel.reading_type == self.reading_type)

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
            data.zone = spec.zone
            data.range_from = spec.range_from
            data.range_to = spec.range_to
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
            data = ThresholdHandlerModel(
                reading_value=threshold, reading_type=self.reading_type)

        with Session(engine, expire_on_commit=True) as session:
            session.add(data)
            session.commit()

        self.threshold = threshold
        self._set_zones_from_threshold()

    def get_threshold(self) -> Optional[ThresholdHandlerModel]:
        try:
            with Session(engine) as session:
                query_statement = select(ThresholdHandlerModel)

                return session.scalars(query_statement).one()
        except NoResultFound:
            return None

    @property
    # @todo specify per reading type
    def zones_spec(self) -> List[ReadingZoneHandlerModel]:
        return [
            ReadingZoneHandlerModel(zone=1, range_from=0, range_to=68,
                                    display_name='Active Recovery', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=2, range_from=68, range_to=83,
                                    display_name='Anaerobic Capacity', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=3, range_from=83,
                                    range_to=95, display_name='Tempo', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=4, range_from=95,
                                    range_to=105, display_name='Threshold', reading_type=self.reading_type),
            ReadingZoneHandlerModel(zone=5, range_from=105,
                                    range_to=200, display_name='VO2 Max', reading_type=self.reading_type),
        ]
