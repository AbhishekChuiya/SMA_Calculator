from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pandas as pd
from .models import FinancialData
import os



class SMACalculator(APIView):

    def get(self, request):
        
        if not FinancialData.objects.exists():
            base_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(base_dir)
            file_path = os.path.join(parent_dir, 'AMBUJACEM-EQ.csv')

            try:
                df = pd.read_csv(file_path)

                df['timestamp'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M:%S%z')

                df.set_index('timestamp', inplace=True)

                full_range_index = pd.date_range(start=df.index.min(), end=df.index.max(), freq='1T')
                df = df.reindex(full_range_index)

                df['Close'].ffill(inplace=True)
            
                for timeframe in ['1T', '2T', '3T', '5T']:
                    resampled_df = df.resample(timeframe).agg({'Close': 'last'})

                    for index, row in resampled_df.iterrows():
                        if pd.isna(row['Close']):
                            print(f"NaN value at index: {index}")
                        financial_data = FinancialData(timeframe=timeframe[0], datetime = index,close=row['Close'])
                        financial_data.save()

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Data uploaded and stored successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Data already uploaded and stored in database'}, status=status.HTTP_200_OK)

    def post(self, request):
        timeframe = request.data.get('timeframe')  
        sma_period = int(request.data.get('sma_period'))  
        
        if timeframe not in ['1', '2', '3', '5']:
            return Response({'error': 'Invalid timeframe provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if sma_period <= 0:
            return Response({'error': 'SMA period should be greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = FinancialData.objects.filter(timeframe=timeframe).order_by('datetime')
            df = pd.DataFrame(list(queryset.values('datetime', 'close')))

            df['datetime'] = df['datetime'].dt.tz_convert('Asia/Kolkata').astype(str)
            
            df['SMA'] = df['close'].rolling(window=sma_period).mean()
            
            df.dropna(inplace=True)
            
            response_data = df.to_dict(orient='records')
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
