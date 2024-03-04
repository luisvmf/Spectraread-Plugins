//MIT License
//
//Copyright (c) 2024 Luis Victor Muller Fabris
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in all
//copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//SOFTWARE.

//Constants
#define Buffersize 700
#define ADCPIN		0

// Defines for setting and clearing register bits

#define clearbit(address, bit) (_SFR_BYTE(address) &= ~ (1 << (bit)))
#define setbit(address, bit) (_SFR_BYTE(address) |= (1 << (bit)))
#define enableadc() setbit(ADCSRA,ADEN);setbit(ADCSRA,ADSC)
#define disableadc() clearbit(ADCSRA,ADEN)
//XXX TODO Voltage ref and check if more prescalers are possible.


//Globals (to share with ISR)
volatile long i=0;
volatile uint16_t triglevel=10;
volatile int triggermode=0;
volatile int trigger=-1;
volatile word DataBuffer[Buffersize];
volatile int beforesamples=0;
volatile int aquisition=0;
volatile int npointsaquire=10;
volatile int localk=0;
volatile int lastdatapoint=0;
volatile int acquiredpre=0;
volatile int currpre=0;
void setup() {
	Serial.begin (1000000);
	clearbit(ADMUX,REFS1);
	setbit(ADMUX,REFS0);
	//setbit(ADMUX,ADLAR);
	ADMUX |= ( ADCPIN & 0x07 );
	clearbit(ADCSRA,ADEN);
	clearbit(ADCSRA,ADSC);
	setbit(ADCSRA,ADATE);
	setbit(ADCSRA,ADIE);
	setbit(ADCSRA,ADPS2);
	setbit(ADCSRA,ADPS1);
	setbit(ADCSRA,ADPS0);
	clearbit(ADCSRB,ACME);
	clearbit(ADCSRB,ADTS2);
	clearbit(ADCSRB,ADTS1);
	clearbit(ADCSRB,ADTS0);
	setbit(DIDR0,ADC5D);
	setbit(DIDR0,ADC4D);
	setbit(DIDR0,ADC3D);
	setbit(DIDR0,ADC2D);
	setbit(DIDR0,ADC1D);
	setbit(DIDR0,ADC0D);
	// Enable ADC
	enableadc();
}

//---------------------------------------
//---------------------------------------
//---------------------------------------
//---------------------------------------
ISR(ADC_vect){
	DataBuffer[i] = word(ADCH,ADCL);
	//Only this if is 28 clock cycles.
		if(trigger==-1){
			acquiredpre=currpre;
			if(triggermode==0){
				if(DataBuffer[i]>triglevel){
					if(DataBuffer[lastdatapoint]<=triglevel){
						if(aquisition==1){
							trigger=i;
							localk=0;
						}
					}
				}
			}
			if(triggermode==1){
				if(DataBuffer[i]<triglevel){
					if(DataBuffer[lastdatapoint]>=triglevel){
						if(aquisition==1){
							trigger=i;
							localk=0;
						}
					}
				}
			}
			if(triggermode==2){
				if(DataBuffer[i]>triglevel){
					if(DataBuffer[lastdatapoint]<=triglevel){
						if(aquisition==1){
							trigger=i;
							localk=0;
						}
					}
				}
				if(DataBuffer[i]<triglevel){
					if(DataBuffer[lastdatapoint]>=triglevel){
						if(aquisition==1){
							trigger=i;
							localk=0;
						}
					}
				}
			}
			lastdatapoint=i;
		}else{
			localk=localk+1;	
			if(localk>npointsaquire){
				localk=-1;
				disableadc();
			}
		}
		i=(i+1);//%Buffersize;
		if(i>=Buffersize){
			i=0;
		}
}
//---------------------------------------
//---------------------------------------
//---------------------------------------

void setprescaler(int prescaler){
	switch(prescaler){
		case 0:
			setbit(ADCSRA,ADPS2);
			setbit(ADCSRA,ADPS1);
			setbit(ADCSRA,ADPS0);//128
			break;
		case 1:
			setbit(ADCSRA,ADPS2);
			setbit(ADCSRA,ADPS1);
			clearbit(ADCSRA,ADPS0);//64
			break;
		case 2:
			setbit(ADCSRA,ADPS2);
			clearbit(ADCSRA,ADPS1);
			setbit(ADCSRA,ADPS0);//32
			break;
		case 3:
			setbit(ADCSRA,ADPS2);
			clearbit(ADCSRA,ADPS1);
			clearbit(ADCSRA,ADPS0);//16
			break;
	}
}


//Read integer from serial port until ndigits is reached or line break \n or \r is found.
int readint(int ndigits){
	char auxarray[ndigits+5];
	for(int k=0;k<ndigits;k++){
		while(Serial.available()<=0){
			delay(1);
		}
		auxarray[k]=Serial.read();
		if(auxarray[k]=='\n'){
			if(k!=0){
				auxarray[k]='\0';
				break;
			}else{
				k=-1;
			}
		}
		if(auxarray[k]=='\r'){
			if(k!=0){
				auxarray[k]='\0';
				break;
			}else{
				k=-1;
			}
		}
		auxarray[k+1]='\0';
	}
	return atoi(auxarray);
}

//MOD operator when b is not negative.
int mod(int a,int b){
	int r=a%b;
	return r<0 ? r + b : r;
}

void loop(){
	char byte;
	int settrig;
	char aux;
	if(Serial.available()>0){
		byte=Serial.read();
		switch(byte){
			case 'c':
				//Serial.println("Start acquisition");//Ok
				aquisition=1;
				break;
			case 'i':
				//Serial.println("Stop acquisition");//Ok
				aquisition=0;
				break;
			case 't':
				//Serial.print("Set trigger:");
				settrig=readint(4);
				if(settrig>1023){
					//Serial.println("Fail");
					break;
				}
				if(settrig<0){
					Serial.println("Fail");
					//break;
				}
				triglevel=settrig;
				//Serial.println(triglevel);
				break;
			case 'm':
				//Serial.print("Trigger mode:");
				while(Serial.available()<=0){
					delay(1);
				}
				aux=Serial.read();
				if(aux!=' '){
					//Serial.println("Fail");
					break;
				}
				while(Serial.available()<=0){
					delay(1);
				}
				aux=Serial.read();
				if(aux!='0'){
					if(aux!='1'){
						if(aux!='2'){
							//Serial.println("Fail");
							break;
						}
					}
				}
				if(aux=='0'){
					//Serial.println("Rising edge");
					triggermode=0;
				}
				if(aux=='1'){
					//Serial.println("Failing edge");
					triggermode=1;
				}
				if(aux=='2'){
					//Serial.println("Rising and failing edge");
					triggermode=2;
				}
				break;
			case 'p':
				//Serial.print("Set prescaler:");
				settrig=readint(1);
				if(settrig>4){
					//Serial.println("Fail");
					break;
				}
				if(settrig<0){
					//Serial.println("Fail");
					break;
				}
				//Serial.println(settrig);
				setprescaler(settrig);
				currpre=settrig;
				break;
			case 'b':
				//Serial.print("Set samples before trigger:");
				settrig=readint(4);
				if(settrig>Buffersize){
					//Serial.println("Fail");
					break;
				}
				if(settrig<0){
					//Serial.println("Fail");
					break;
				}
				//Serial.println(settrig);
				beforesamples=settrig;
				break;
			case 'n':
				//Serial.print("Set number of points to aquire:");
				settrig=readint(4);
				if(settrig>Buffersize-3){
					//Serial.println("Fail, must be smaller than Buffersize-3");
					break;
				}
				if(settrig<10){
					//Serial.println("Fail, must be larger than 10");
					break;
				}
				//Serial.println(settrig);
				npointsaquire=settrig;
				break;
			case 's'://Ok
				//Serial.println("Single run");
				localk=0;
				trigger=i;
				break;
		}
	}
	volatile int j=trigger;
	int n=0;
	j=mod((j-beforesamples),Buffersize);
	if(localk==-1){
		if(trigger!=-1){
			Serial.print("Data:");
			Serial.println(npointsaquire);
			Serial.println(acquiredpre);
			while(n<npointsaquire){
				Serial.write(lowByte(DataBuffer[j]));
				Serial.write(highByte(DataBuffer[j]));
				j=mod((j+1),Buffersize);
				n=n+1;
			}
			delay(1);//Hold
			trigger=-1;
			localk=0;
			enableadc();
		}
	}
	delay(1);
}
