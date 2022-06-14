from domain.dataset import FulfillmentMode
from typing import Dict, Optional, List, Any
from pydantic import BaseModel
from domain.filler import MeanValueFiller, MedianValueFiller
from domain.pca_transformer import PCATransformer
from domain.dataset import Dataset


class PreprocessingOptions(BaseModel):
    fulfillment_mode: FulfillmentMode
    columns_to_fulfill: List[str]
    target_column: List
    n_components: int


class FillerMetadata(BaseModel):
    filler_type: str
    filler_value: Dict[str, float]


class TargetMetadata(BaseModel):
    target_column: List


class TransformerMetadata(BaseMode):
    scaler: Any


class MetadataDo(BaseModel):
    # filler_metadata: FillerMetadata
    # target_metadata: TargetMetadata
    # transformer_metadata: TransformerMetadata
    filler_metadata: Any
    target_metadata: Any
    transformer_metadata: Any

    def to_dict(self):
        return {
            'filler_metadata':
            {
                'filler_type': self.filler_metadata['filler_type'].value,
                'filler_value': self.filler_metadata['filler_value']
            },
            'target_metadata':
            {
                'target_column': self.target_metadata
            },
            'transformer_metadata':
            {
                'scaler': self.transformer_metadata['scaler'],
                'n_components': self.transformer_metadata['n_components']
            },
        }

    def from_dict(dict):
        return MetadataDo(
            filler_metadata=dict['filler_metadata'],
            target_metadata=dict['target_metadata'],
            transformer_metadata=dict['transformer_metadata']
        )


class PreprocessingService:
    def preprocess(self,
                   dataset: Dataset,
                   fulfillment_mode: FulfillmentMode,
                   columns_to_fulfill: List[str],
                   target_column: List,
                   n_components: int,
                   metadata_do: Optional[MetadataDo] = None,
                   ):
        if dataset is None:
            raise Exception("The dataset is empty")
        filler_metadata = metadata_do.filler_metadata if metadata_do is not None else None
        transformer_metadata = metadata_do.transformer_metadata if metadata_do is not None else None

        filler = self._determine_filler(
            fulfillment_mode=fulfillment_mode,
            filler_metadata=filler_metadata,
        )
        dataset.fulfill_missing_values(
            filler=filler,
            columns_to_fulfill=columns_to_fulfill,
        )
        dataset.change_target_to_numeric(
            columns_to_change=target_column,
        )
        PCA_transformer = PCATransformer(metadata=transformer_metadata)

        dataset.transform_with_PCA(
            transformer=PCA_transformer,
            target_column=target_column,
            n_components=n_components,
        )

        return MetadataDo(filler_metadata=filler.metadata(),
                          target_metadata=target_column,
                          transformer_metadata=PCA_transformer.metadata()
                          )

    def _determine_filler(self, fulfillment_mode: FulfillmentMode,
                          filler_metadata):
        if fulfillment_mode == FulfillmentMode.MEAN:
            return MeanValueFiller(metadata=filler_metadata)
        if fulfillment_mode == FulfillmentMode.MEDIAN:
            return MedianValueFiller(metadata=filler_metadata)
